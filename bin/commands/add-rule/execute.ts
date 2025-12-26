import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { Output } from "../_shared/schema";
import { generateSimHash } from "../_shared/simhash";
import { createRuleMarkdown, RuleFrontmatter } from "../_shared/frontmatter";
import { addRuleInput } from "./types";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function sanitizeFileName(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .trim();
}

export async function addRuleHandler(
  input: z.infer<typeof addRuleInput>
): Promise<Output> {
  try {
    const rootDir = path.resolve(__dirname, "../../..");
    const rulesDir = path.join(rootDir, ".agent", "rules");

    // Ensure rules directory exists
    if (!fs.existsSync(rulesDir)) {
      fs.mkdirSync(rulesDir, { recursive: true });
    }

    // Sanitize and create filename
    const fileName = sanitizeFileName(input.name) + ".md";
    const filePath = path.join(rulesDir, fileName);

    // Check if file already exists
    if (fs.existsSync(filePath)) {
      return {
        error: `Rule already exists: ${fileName}. Use a different name or delete the existing rule first.`,
        data: null,
      };
    }

    // Parse tags
    const tags = input.tags
      .split(",")
      .map((t) => t.trim().toLowerCase())
      .filter((t) => t.length > 0);

    if (tags.length === 0) {
      return {
        error: "At least one tag is required",
        data: null,
      };
    }

    // Generate SimHash from content + title + tags for better semantic matching
    const hashInput = [
      input.title || input.name,
      input.content,
      ...tags,
    ].join(" ");
    const simhash = generateSimHash(hashInput);

    // Create frontmatter
    const frontmatter: RuleFrontmatter = {
      title: input.title || input.name,
      tags,
      simhash,
      created: new Date().toISOString().split("T")[0],
    };

    // Create full markdown content
    const markdown = createRuleMarkdown(frontmatter, input.content);

    // Write file
    fs.writeFileSync(filePath, markdown, "utf-8");

    return {
      error: null,
      data: JSON.stringify(
        {
          message: "Rule created successfully",
          file: fileName,
          path: filePath,
          frontmatter,
        },
        null,
        2
      ),
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : String(error),
      data: null,
    };
  }
}
