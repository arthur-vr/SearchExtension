import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { z } from "zod";
import { Output } from "../_shared/schema";
import { updateRuleInput } from "./types";

const MARKER = "### FROM_ROOT_RULES ###";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

function shareRootRules(
  sourceFilePath: string,
  targetFiles: string[],
  marker: string = MARKER
): { created: string[]; updated: string[]; skipped: string[] } {
  const sourceContent = fs.readFileSync(sourceFilePath, "utf-8");
  const created: string[] = [];
  const updated: string[] = [];
  const skipped: string[] = [];

  targetFiles.forEach((targetPath) => {
    if (!fs.existsSync(targetPath)) {
      const parentDir = path.dirname(targetPath);
      fs.mkdirSync(parentDir, { recursive: true });
      const newContent = `${marker}\n\n${sourceContent}`;

      fs.writeFileSync(targetPath, newContent, "utf-8");
      created.push(targetPath);
      return;
    }

    const targetContent = fs.readFileSync(targetPath, "utf-8");
    const markerIndex = targetContent.indexOf(marker);

    if (markerIndex === -1) {
      skipped.push(targetPath);
      return;
    }

    const updatedContent = `${targetContent.slice(0, markerIndex + marker.length)}\n\n${sourceContent}`;

    if (updatedContent === targetContent) {
      skipped.push(targetPath);
      return;
    }

    fs.writeFileSync(targetPath, updatedContent, "utf-8");
    updated.push(targetPath);
  });

  return { created, updated, skipped };
}

export async function updateRuleHandler(
  _input: z.infer<typeof updateRuleInput>
): Promise<Output> {
  try {
    const rootDir = path.resolve(__dirname, "../../..");
    const sourceFile = path.join(rootDir, ".agent", "root-rules.md");
    const targetFiles = [
      path.join(rootDir, ".cursor", "rules", "root-rules.mdc"),
      path.join(rootDir, ".cursorrules"),
      path.join(rootDir, ".clinerules"),
      path.join(rootDir, "CLAUDE.md"),
      path.join(rootDir, ".windsurfrules"),
      path.join(rootDir, ".github", "copilot-instructions.md"),
      path.join(rootDir, "AGENTS.md"),
      path.join(rootDir, "GEMINI.md"),
      path.join(rootDir, ".aider.instructions.md"),
    ];

    const result = shareRootRules(sourceFile, targetFiles, MARKER);

    return {
      error: null,
      data: JSON.stringify(result, null, 2),
    };
  } catch (error) {
    return {
      error: error instanceof Error ? error.message : String(error),
      data: null,
    };
  }
}
