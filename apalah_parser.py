class ApalahToken():
    token : 'str' = None
    binary : 'int' = None # Untuk nanti dipake di operasi boolean
    is_symbol : bool = None

    def set_binary(self, b : 'int'):
        self.binary = b
    
    def __str__(self) -> str:
        return f"{self.token} ({self.binary})"

class ApalahParser():
    __symbol_used: 'str' = "&|()~ "
    token: 'list[ApalahToken]' = None

    def __init__(self) -> None:
        self.token = []

    @staticmethod
    def parse(query: 'str') -> 'ApalahParser':
        q = query.strip()

        tokens: 'list[str]' = []
        startpos: 'int' = 0

        for i, letter in enumerate(q):
            if letter in ApalahParser.__symbol_used:
                tokens.append(q[startpos:i])
                tokens.append(letter)
                startpos = i + 1

        if startpos != 0:
            tokens.append(q[startpos:len(q)])
        else:
            tokens.append(q)

        # Hapus leading dan trailing spasi
        for i, it in enumerate(tokens):
            tokens[i] = it.strip()

        # Hapus token kosong
        v_token: 'list[str]' = []
        for i, it in enumerate(tokens):
            if len(it) > 0:
                v_token.append(it)

        # Pastikan ( dan ) balance
        if v_token.count("(") != v_token.count(")"):
            print("Ada kurung buka yang tidak ditutup")
            return
        
        p = ApalahParser()
        for i, it in enumerate(v_token):
            a = ApalahToken()
            a.token = it
            a.is_symbol = it in ApalahParser.__symbol_used
            p.token.append(a)

        return p