class Db:
    
    @staticmethod
    def create_tables():
        """create all require tables"""
        querys = [
            "CREATE TABLE IF NOT EXISTS general (id bigint primary key, prefix varchar(5));",
            "CREATE TABLE IF NOT EXISTS codes (id bigint primary key, code1 text, code2 text, code3 text, code4 text, code5 text);",
            "CREATE TABLE IF NOT EXISTS tags (tag varchar(50) primary key, id bigint, text text);"
        ]
        return querys