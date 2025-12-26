/**
 * Frontmatter parser and generator for Markdown files
 */

export interface RuleFrontmatter {
  tags: string[];
  simhash: string;
  title?: string;
  created?: string;
}

export interface ParsedRule {
  frontmatter: RuleFrontmatter;
  content: string;
  raw: string;
}

const FRONTMATTER_REGEX = /^---\n([\s\S]*?)\n---\n([\s\S]*)$/;

/**
 * Parse frontmatter from markdown content
 */
export function parseFrontmatter(content: string): ParsedRule | null {
  const match = content.match(FRONTMATTER_REGEX);
  if (!match) {
    return null;
  }

  const [, yamlContent, body] = match;
  const frontmatter: RuleFrontmatter = {
    tags: [],
    simhash: "",
  };

  // Simple YAML parser for our specific format
  const lines = yamlContent.split("\n");
  for (const line of lines) {
    const tagMatch = line.match(/^tags:\s*\[(.*)\]$/);
    if (tagMatch) {
      frontmatter.tags = tagMatch[1]
        .split(",")
        .map((t) => t.trim().replace(/['"]/g, ""))
        .filter((t) => t.length > 0);
      continue;
    }

    const simhashMatch = line.match(/^simhash:\s*["']?([a-f0-9]+)["']?$/);
    if (simhashMatch) {
      frontmatter.simhash = simhashMatch[1];
      continue;
    }

    const titleMatch = line.match(/^title:\s*["']?(.+?)["']?$/);
    if (titleMatch) {
      frontmatter.title = titleMatch[1];
      continue;
    }

    const createdMatch = line.match(/^created:\s*["']?(.+?)["']?$/);
    if (createdMatch) {
      frontmatter.created = createdMatch[1];
      continue;
    }
  }

  return {
    frontmatter,
    content: body.trim(),
    raw: content,
  };
}

/**
 * Generate frontmatter string
 */
export function generateFrontmatter(frontmatter: RuleFrontmatter): string {
  const lines = ["---"];

  if (frontmatter.title) {
    lines.push(`title: "${frontmatter.title}"`);
  }

  lines.push(`tags: [${frontmatter.tags.map((t) => `"${t}"`).join(", ")}]`);
  lines.push(`simhash: "${frontmatter.simhash}"`);

  if (frontmatter.created) {
    lines.push(`created: "${frontmatter.created}"`);
  }

  lines.push("---");
  return lines.join("\n");
}

/**
 * Create full markdown with frontmatter
 */
export function createRuleMarkdown(
  frontmatter: RuleFrontmatter,
  content: string
): string {
  return `${generateFrontmatter(frontmatter)}\n\n${content}`;
}
