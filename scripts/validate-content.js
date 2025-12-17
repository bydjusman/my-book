#!/usr/bin/env node

// Script to validate content according to textbook standards
// Checks word count, Markdown structure, and basic requirements

const fs = require('fs');
const path = require('path');

// Configuration
const MIN_WORDS = 1500;
const MAX_WORDS = 2000;
const VALID_DIRS = [
  'docs/module-1-ros2',
  'docs/module-2-simulation',
  'docs/module-3-perception',
  'docs/module-4-vla'
];

function countWords(text) {
  return text.trim()
    .split(/\s+/)
    .filter(word => word.length > 0).length;
}

function validateFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const words = countWords(content);

    const isValid = words >= MIN_WORDS && words <= MAX_WORDS;

    console.log(`${isValid ? '✓' : '✗'} ${filePath} - ${words} words (${isValid ? 'OK' : 'INVALID'})`);

    if (!isValid) {
      if (words < MIN_WORDS) {
        console.log(`  ⚠ Content is too short. Minimum: ${MIN_WORDS} words, Actual: ${words} words`);
      }
      if (words > MAX_WORDS) {
        console.log(`  ⚠ Content is too long. Maximum: ${MAX_WORDS} words, Actual: ${words} words`);
      }
    }

    return { isValid, words };
  } catch (error) {
    console.error(`Error reading ${filePath}:`, error.message);
    return { isValid: false, words: 0 };
  }
}

function validateDirectory(dirPath) {
  console.log(`\nValidating directory: ${dirPath}`);
  console.log('----------------------------------------');

  if (!fs.existsSync(dirPath)) {
    console.log(`Directory does not exist: ${dirPath}`);
    return { validFiles: 0, totalFiles: 0, totalWords: 0 };
  }

  const files = fs.readdirSync(dirPath).filter(file =>
    path.extname(file) === '.md' && file !== 'index.md'
  );

  let validFiles = 0;
  let totalWords = 0;

  for (const file of files) {
    const filePath = path.join(dirPath, file);
    const result = validateFile(filePath);

    if (result.isValid) {
      validFiles++;
    }
    totalWords += result.words;
  }

  return {
    validFiles,
    totalFiles: files.length,
    totalWords
  };
}

function main() {
  console.log('Content Validation Tool');
  console.log('Validating textbook modules for word count compliance');
  console.log(`Requirements: ${MIN_WORDS}-${MAX_WORDS} words per module section`);
  console.log('====================================================');

  let totalValid = 0;
  let totalFiles = 0;
  let totalWords = 0;

  for (const dir of VALID_DIRS) {
    const result = validateDirectory(dir);
    totalValid += result.validFiles;
    totalFiles += result.totalFiles;
    totalWords += result.totalWords;
  }

  console.log('\n====================================================');
  console.log('SUMMARY');
  console.log(`Total files validated: ${totalFiles}`);
  console.log(`Valid files: ${totalValid}`);
  console.log(`Invalid files: ${totalFiles - totalValid}`);
  console.log(`Total words across all files: ${totalWords}`);

  if (totalFiles > 0) {
    const successRate = ((totalValid / totalFiles) * 100).toFixed(1);
    console.log(`Success rate: ${successRate}%`);

    if (totalValid === totalFiles) {
      console.log('✓ All content meets validation requirements!');
      process.exit(0);
    } else {
      console.log('✗ Some content does not meet validation requirements.');
      process.exit(1);
    }
  } else {
    console.log('No content files found to validate.');
    process.exit(0);
  }
}

if (require.main === module) {
  main();
}