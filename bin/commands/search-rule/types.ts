import { z } from "zod";

export const searchRuleInput = z.object({
  query: z.string().describe("Search query text"),
  tags: z.string().optional().describe("Comma-separated tags to filter by"),
  limit: z.string().optional().default("10").describe("Max results to return"),
  detail: z.string().optional().describe("Show detailed output (scores, preview)"),
});

export type SearchRuleInput = z.infer<typeof searchRuleInput>;
