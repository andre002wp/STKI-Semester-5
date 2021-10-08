class ApalahParser():
    query : 'list[str]' = None

    @staticmethod
    def parse(query: 'str'):
        q = query.strip()

        tokens: 'list[str]' = []
        startpos: 'int' = 0

        for i, letter in enumerate(q):
            if letter in "&|()~ ":
                tokens.append(q[startpos:i])
                tokens.append(letter)
                startpos = i + 1

        if startpos != 0:
            tokens.append(q[startpos:len(q)])

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
        p.query = v_token
        
