/**
 * SimHash implementation for locality-sensitive hashing
 * Similar texts will produce similar hash values
 */

const HASH_BITS = 64;

// Simple string hash function (FNV-1a like)
function hashToken(token: string): bigint {
  let hash = BigInt(0xcbf29ce484222325n);
  for (let i = 0; i < token.length; i++) {
    hash ^= BigInt(token.charCodeAt(i));
    hash *= BigInt(0x100000001b3n);
  }
  return hash;
}

// Tokenize text into n-grams
function tokenize(text: string, ngramSize: number = 3): string[] {
  const normalized = text.toLowerCase().replace(/[^\w\s]/g, " ");
  const words = normalized.split(/\s+/).filter((w) => w.length > 0);
  const tokens: string[] = [];

  // Word unigrams
  tokens.push(...words);

  // Word bigrams
  for (let i = 0; i < words.length - 1; i++) {
    tokens.push(`${words[i]} ${words[i + 1]}`);
  }

  // Character n-grams for each word
  for (const word of words) {
    if (word.length >= ngramSize) {
      for (let i = 0; i <= word.length - ngramSize; i++) {
        tokens.push(word.slice(i, i + ngramSize));
      }
    }
  }

  return tokens;
}

/**
 * Generate SimHash for a given text
 */
export function generateSimHash(text: string): string {
  const tokens = tokenize(text);
  const vector: number[] = new Array(HASH_BITS).fill(0);

  for (const token of tokens) {
    const hash = hashToken(token);
    for (let i = 0; i < HASH_BITS; i++) {
      if ((hash >> BigInt(i)) & 1n) {
        vector[i]++;
      } else {
        vector[i]--;
      }
    }
  }

  // Convert to binary hash
  let result = 0n;
  for (let i = 0; i < HASH_BITS; i++) {
    if (vector[i] > 0) {
      result |= 1n << BigInt(i);
    }
  }

  return result.toString(16).padStart(16, "0");
}

/**
 * Calculate Hamming distance between two SimHash values
 * Lower distance = more similar
 */
export function hammingDistance(hash1: string, hash2: string): number {
  const a = BigInt(`0x${hash1}`);
  const b = BigInt(`0x${hash2}`);
  let xor = a ^ b;
  let count = 0;

  while (xor > 0n) {
    count += Number(xor & 1n);
    xor >>= 1n;
  }

  return count;
}

/**
 * Calculate similarity score (0-1) based on Hamming distance
 * 1 = identical, 0 = completely different
 */
export function similarity(hash1: string, hash2: string): number {
  const distance = hammingDistance(hash1, hash2);
  return 1 - distance / HASH_BITS;
}
