import { z } from "zod";

export const addRuleInput = z.object({
  name: z.string().describe("Rule file name (without .md extension)"),
  title: z.string().optional().describe("Rule title"),
  tags: z.string().describe("Comma-separated tags for the rule"),
  content: z.string().describe("Rule content (markdown)"),
});

export type AddRuleInput = z.infer<typeof addRuleInput>;
