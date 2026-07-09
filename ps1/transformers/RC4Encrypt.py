import os
from utils.utils import bytes_to_ps1
from Crypto.Cipher import ARC4
import string
import random

class RC4Encrypt:

    def __init__(self):
        self.name = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(16))
        self.key = os.urandom(16)

    def compilerOptions(self):
        return []

    def imports(self):
        return []

    def codeblock(self):
        return """
function {name} {{
    [CmdletBinding()]
    [OutputType([byte[]])]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [byte[]]$CipherBytes
    )
    begin {{
        $buffer = [System.Collections.Generic.List[byte]]::new()
    }}
    process {{
        $buffer.AddRange($CipherBytes)
    }}
    end {{

        {key}
        [byte[]]$S = 0..255
        [int]$j = 0
        for ([int]$i = 0; $i -lt 256; $i++) {{
            $j = ($j + $S[$i] + $Key[$i % $Key.Length]) % 256
            $temp = $S[$i]
            $S[$i] = $S[$j]
            $S[$j] = $temp
        }}

        [byte[]]$Output = New-Object byte[] $CipherBytes.Length
        [int]$i = 0
        [int]$j = 0
        for ([int]$k = 0; $k -lt $CipherBytes.Length; $k++) {{
            $i = ($i + 1) % 256
            $j = ($j + $S[$i]) % 256
            
            # Swap values
            $temp = $S[$i]
            $S[$i] = $S[$j]
            $S[$j] = $temp

            $t = ($S[$i] + $S[$j]) % 256
            $Output[$k] = $CipherBytes[$k] -bxor $S[$t]
        }}

        return $Output

    }}
}}
""".format(name=self.name, key = bytes_to_ps1(self.key, 'Key'))

    def encode(self, plaintext):
        self.shellcodeSize = len(plaintext)
        cipher = ARC4.new(self.key)
        return cipher.encrypt(plaintext)

    def transformer(self, shellcodestring):
        return shellcodestring.format(shellcode=f'{self.name}({{shellcode}})')