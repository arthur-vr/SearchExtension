import { z } from "zod";

export const updateRuleInput = z.object({
  // 現在オプションなし
});

export type UpdateRuleInput = z.infer<typeof updateRuleInput>;
