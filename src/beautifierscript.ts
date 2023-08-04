function splitTokens(code: string, delimiters: string[]): string[] {
  const parts: string[] = [];
  let startIndex = 0;
  let currentIndex = 0;

  while (currentIndex < code.length) {
    let currentChar = code[currentIndex];
    if (delimiters.includes(currentChar)) {
      if (currentIndex > startIndex) {
        const part = code.substring(startIndex, currentIndex);
        parts.push(part + currentChar);
      }
      startIndex = currentIndex + 1;
    } else {
      const part = code.substring(startIndex, currentIndex);
      if (part.trim() === 'return') {
        const savePos = currentIndex;
        currentIndex = currentIndex + 1;
        currentChar = code[currentIndex];
        let stringCheck = false;
        if (currentChar === '"') {
          stringCheck = true;
          currentIndex = currentIndex + 1;
          currentChar = code[currentIndex];
        }
        if (currentChar === '(') {
          currentIndex = currentIndex + 1;
          currentChar = code[currentIndex];
        }
        while (currentIndex < code.length) {
          currentIndex = currentIndex + 1;
          if (
            currentChar === '"' ||
            currentChar === ')' ||
            (currentChar === ' ' && !stringCheck)
          ) {
            break;
          }
          currentChar = code[currentIndex];
        }
        const part = code.substring(savePos, currentIndex);
        parts.push('return' + part + '\n');
        startIndex = currentIndex ;
      }
    }
    currentIndex++;
  }
  if (currentIndex > startIndex) {
    const lastPart = code.substring(startIndex, currentIndex);
    parts.push(lastPart);
  }
  return parts;
}


export function beautifyPythonCode(code: string): string {
  let beautifiedCode = '';
  let indentLevel = 0;

  const lines = splitTokens(code, [',', ':', '|', '\n']);
  const regexIndentIncrease = /^(\s*)(if|for|while|def|class|else|elif).*:/;
  const regexIndentDecrease = /^(\s*)(else|elif).*:/;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();

    if (regexIndentDecrease.test(line)) {
      indentLevel = Math.max(0, indentLevel - 1); // Ensure indentLevel is non-negative
    }

    if (line.endsWith(':')) {
      beautifiedCode += '    '.repeat(indentLevel) + line + '\n';
      if (regexIndentIncrease.test(line)) {
        indentLevel++;
      }
    } else {
      beautifiedCode += '    '.repeat(indentLevel) + line + '\n';
    }
  }

  return beautifiedCode;
}