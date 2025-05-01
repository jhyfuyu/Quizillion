UPDATE  quiz2 SET unique_key='qk14sd41ss' WHERE id=1;
UPDATE  quiz3 SET channel='https://t.me/MemecoinOK';


UPDATE quiz3
SET (question, answers, correct) = (
    SELECT 
        CASE id
            WHEN 1 THEN 'What are ''Memecoins''?'
            WHEN 2 THEN 'Meme coins are known for their:'
            WHEN 3 THEN 'What purpose do Memecoins serve beyond currency?'
            WHEN 4 THEN 'What mindset is encouraged when encountering Memecoins?'
            WHEN 5 THEN 'Which meme coin was created as a parody of Bitcoin and features a Shiba Inu dog as its logo?'
            WHEN 6 THEN 'What is the founder of Dogecoin''s name, who initially created it as a joke?'
            WHEN 7 THEN 'Which blockchain platform is often used for creating meme coins and non-fungible tokens (NFTs) in 2024?'
            WHEN 8 THEN 'Which memecoin features a green frog?'
            WHEN 9 THEN 'Top memecoin by market capitalization?'
            WHEN 10 THEN 'They attract diverse individuals'
        END AS question,
        CASE id
            WHEN 1 THEN 'A cryptocurrency that only exists in meme format Social media profiles, A cryptocurrency that uses popular internet memes as its logo, A cryptocurrency that started as a joke or meme but gained real value and popularity, A cryptocurrency used exclusively for memes on social media'
            WHEN 2 THEN 'High security features, Stable and predictable value\n3. Volatile and speculative nature, Strong regulatory oversight'
            WHEN 3 THEN 'They serve as digital collectibles, They predict stock market trends, They fund charitable organisations, They foster cultural communities'
            WHEN 4 THEN 'Prioritize financial gain over cultural value, Treat Memecoins as traditional investments, Focus solely on monetary returns, Prioritize cultural and community value over monetary gain'
            WHEN 5 THEN 'Dogecoin (DOGE), Ethereum (ETH), Ripple (XRP), Litecoin (LTC)'
            WHEN 6 THEN 'Satoshi Nakamoto, Mark Zuckerberg, Billy Markus, Vitalik Buterin'
            WHEN 7 THEN 'Ethereum (ETH), Bitcoin (BTC), Binance Coin (BNB), Solana (SOL)'
            WHEN 8 THEN 'MEME, PEPE, BEBE, HEHE'
            WHEN 9 THEN 'Shiba Inu, PEPE, Dogecoin, Bonk'
            WHEN 10 THEN 'A dance move, A decentralised App, An Ethereum token, A dog breed'
        END AS answers,
        CASE id
            WHEN 1 THEN 2
            WHEN 2 THEN 2
            WHEN 3 THEN 3
            WHEN 4 THEN 3
            WHEN 5 THEN 2
            WHEN 6 THEN 0
            WHEN 7 THEN 2
            WHEN 8 THEN 3
            WHEN 9 THEN 1
            WHEN 10 THEN 2
        END AS correct
    )
WHERE id IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10);


