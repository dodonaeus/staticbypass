import random
import string

class Brainfuck:

    def __init__(self):
        self.name = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(16))

    def imports(self):
        return []

    def codeblock(self):
        return """
unsigned char * {name}(unsigned char *encoded)
{{
    unsigned char *out = calloc({size}, sizeof(unsigned char));
    int j = 0;
    for (int i =0; i < strlen(encoded); i++){{
        if (encoded[i] == '>'){{
            j++;
        }} else if (encoded[i] == '+'){{
            out[j] += 1;
        }}
    }}

    return out;
}}
""".format(name = self.name, size = self.size)
    
    def compilerOptions(self):
        return []

    def obfuscate(self, decoded):
        self.size = len(decoded)
        encoded = '>'.join(['+'*decoded[i] for i in range(0, len(decoded))])
        return encoded

    def transformer(self, shellcodestring):
        return shellcodestring.format(shellcode=f'{self.name}({{shellcode}})')