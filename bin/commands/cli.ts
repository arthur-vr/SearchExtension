import { z } from "zod";
import { OutputSchema } from "./_shared/schema";

import * as buildFunction from "./build";
import * as updateRuleFunction from "./update-rule";
import * as searchRuleFunction from "./search-rule";
import * as addRuleFunction from "./add-rule";

//
// 1. Register Commands
//
const commands = {
  build: {
    input: buildFunction.buildInput,
    handler: buildFunction.buildHandler,
  },
  "update-rule": {
    input: updateRuleFunction.updateRuleInput,
    handler: updateRuleFunction.updateRuleHandler,
  },
  "search-rule": {
    input: searchRuleFunction.searchRuleInput,
    handler: searchRuleFunction.searchRuleHandler,
  },
  "add-rule": {
    input: addRuleFunction.addRuleInput,
    handler: addRuleFunction.addRuleHandler,
  },
} as const;

//
// 2. Flag Parser
//
function parseFlags(args: string[]) {
  const out: Record<string, string> = {};
  let key: string | null = null;

  for (const arg of args) {
    if (arg.startsWith("--")) {
      // If previous key had no value, treat as boolean flag
      if (key) {
        out[key] = "true";
      }
      key = arg.slice(2);
    } else if (key) {
      out[key] = arg;
      key = null;
    }
  }
  // Handle trailing flag with no value
  if (key) {
    out[key] = "true";
  }
  return out;
}

//
// 3. CLI Execution
//
async function main() {
  const [, , cmdName, ...rawArgs] = process.argv;

  if (!cmdName) {
    console.error("Please provide a command name.");
    console.error(`Available commands: ${Object.keys(commands).join(", ")}`);
    process.exit(1);
  }

  const cmd = commands[cmdName as keyof typeof commands];
  if (!cmd) {
    console.error(`Unknown command: ${cmdName}`);
    console.error(`Available commands: ${Object.keys(commands).join(", ")}`);
    process.exit(1);
  }

  const flags = parseFlags(rawArgs);
  const parsedInput = cmd.input.safeParse(flags);

  if (!parsedInput.success) {
    const message = parsedInput.error.issues
      .map((e) => `${e.path.join(".")}: ${e.message}`)
      .join("\n");

    console.error(message);
    process.exit(1);
  }

  const output = await cmd.handler(parsedInput.data);

  const parsedOutput = OutputSchema.safeParse(output);
  if (!parsedOutput.success) {
    console.error("Invalid output format");
    process.exit(1);
  }

  if (parsedOutput.data.error) {
    console.error(parsedOutput.data.error);
    process.exit(1);
  } else {
    console.log(parsedOutput.data.data ?? "");
    process.exit(0);
  }
}

main().catch((err) => {
  console.error(String(err));
  process.exit(1);
});
