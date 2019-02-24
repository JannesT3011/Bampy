class Db:
    @staticmethod
    def create_tables():
        """Create all require tables"""
        querys = [
            "CREATE TABLE IF NOT EXISTS setup (server_id bigint primary key not null, userjoin_leave boolean, servertags boolean, modlog boolean, meme boolean, counter boolean, mod boolean, games boolean, nsfw boolean, edu boolean, social boolean);",
            "CREATE TABLE IF NOT EXISTS tags (server_id bigint primary key not null, name varchar(50), text text);",
            "CREATE TABLE IF NOT EXISTS server_stuff (server_id bigint primary key not null, userjoin_msg varchar(1700), userleave_msg varchar(1700), memechannel bigint, counterchannel bigint);",
            "CREATE TABLE IF NOT EXISTS general (id bigint primary key not null, prefix varchar(15));"
        ]

        return querys