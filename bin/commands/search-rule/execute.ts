import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { Output } from "../_shared/schema";
import { generateSimHash, similarity } from "../_shared/simhash";
import { parseFrontmatter, ParsedRule } from "../_shared/frontmatter";
import { searchRuleInput } from "./types";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

interface SearchResultSimple {
  file: string;
  title: string;
}

interface SearchResultDetailed extends SearchResultSimple {
  tags: string[];
  score: number;
  scoreBreakdown: {
    simhash: number;
    tagMatch: number;
    textMatch: number;
  };
  preview: string;
}

function getAllRuleFiles(rulesDir: string): string[] {
  if (!fs.existsSync(rulesDir)) {
    return [];
  }

  const files: string[] = [];
  const entries = fs.readdirSync(rulesDir, { withFileTypes: true });

  for (const entry of entries) {
    if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(path.join(rulesDir, entry.name));
    }
  }

  return files;
}

function loadRule(filePath: string): ParsedRule | null {
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    return parseFrontmatter(content);
  } catch {
    return null;
  }
}

function calculateTextMatchScore(query: string, content: string): number {
  const queryLower = query.toLowerCase();
  const contentLower = content.toLowerCase();

  // Check for exact phrase match
  if (contentLower.includes(queryLower)) {
    return 1.0;
  }

  // Check for word matches
  const queryWords = queryLower.split(/\s+/).filter((w) => w.length > 2);
  if (queryWords.length === 0) return 0;

  let matchedWords = 0;
  for (const word of queryWords) {
    if (contentLower.includes(word)) {
      matchedWords++;
    }
  }

  return matchedWords / queryWords.length;
}

function calculateTagMatchScore(
  queryTags: string[],
  ruleTags: string[]
): number {
  if (queryTags.length === 0) return 0;

  const ruleTagsLower = ruleTags.map((t) => t.toLowerCase());
  let matchedTags = 0;

  for (const tag of queryTags) {
    if (ruleTagsLower.includes(tag.toLowerCase())) {
      matchedTags++;
    }
  }

  return matchedTags / queryTags.length;
}

export async function searchRuleHandler(
  input: z.infer<typeof searchRuleInput>
): Promise<Output> {
  try {
    const rootDir = path.resolve(__dirname, "../../..");
    const rulesDir = path.join(rootDir, ".agent", "rules");
    const limit = parseInt(input.limit || "10", 10);

    const ruleFiles = getAllRuleFiles(rulesDir);

    if (ruleFiles.length === 0) {
      return {
        error: null,
        data: JSON.stringify({
          message: "No rules found in .agent/rules/",
          results: [],
        }),
      };
    }

    const querySimHash = generateSimHash(input.query);
    const queryTags = input.tags
      ? input.tags.split(",").map((t) => t.trim())
      : [];
    const showDetail = input.detail !== undefined;

    const results: SearchResultDetailed[] = [];

    for (const filePath of ruleFiles) {
      const rule = loadRule(filePath);
      if (!rule) continue;

      const fileName = path.basename(filePath);

      // Calculate scores
      const simhashScore = rule.frontmatter.simhash
        ? similarity(querySimHash, rule.frontmatter.simhash)
        : 0;

      const tagMatchScore = calculateTagMatchScore(
        queryTags,
        rule.frontmatter.tags
      );

      const textMatchScore = calculateTextMatchScore(
        input.query,
        `${fileName} ${rule.frontmatter.title || ""} ${rule.content}`
      );

      // Weighted combined score
      // Text match: 0.5, SimHash: 0.3, Tags: 0.2
      const combinedScore =
        textMatchScore * 0.5 + simhashScore * 0.3 + tagMatchScore * 0.2;

      // Preview: first 150 chars of content
      const preview =
        rule.content.slice(0, 150).replace(/\n/g, " ") +
        (rule.content.length > 150 ? "..." : "");

      results.push({
        file: fileName,
        title: rule.frontmatter.title || fileName.replace(".md", ""),
        tags: rule.frontmatter.tags,
        score: Math.round(combinedScore * 100) / 100,
        scoreBreakdown: {
          simhash: Math.round(simhashScore * 100) / 100,
          tagMatch: Math.round(tagMatchScore * 100) / 100,
          textMatch: Math.round(textMatchScore * 100) / 100,
        },
        preview,
      });
    }

    // Sort by score (descending) and limit
    results.sort((a, b) => b.score - a.score);
    const limitedResults = results.slice(0, limit);

    // Format output based on detail flag
    const outputResults = showDetail
      ? limitedResults
      : limitedResults.map(({ file, title }) => ({ file, title }));

    const outputData = showDetail
      ? {
          query: input.query,
          querySimHash,
          totalRules: ruleFiles.length,
          returnedCount: limitedResults.length,
          results: outputResults,
        }
      : {
          results: outputResults,
        };

    return {
      error: null,
      data: JSON.stringify(outputData, null, 2),
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : String(error),
      data: null,
    };
  }
}
