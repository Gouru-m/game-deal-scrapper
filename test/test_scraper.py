from app.deals.scraper import parse_deals

def test_parse_deals_extract_game_cards():
    html = """
    <html>
        <body>
            <div class="game-card">
                <a href="/game/test-game">
                    <img src="/images/test.jpg">
                    <span class="game-title">Test Game</span>
                </a>
                <span class="genre">Action</span>
                <span class="original-price">$29.99</span>
                <span class="sale-price">$10.00</span>
            </div>
        </body>
    </html>
    """

    deals = parse_deals(
        html=html,
        base_url="https://example.com",
        source="test_source"
    )

    assert len(deals) == 1
    assert deals[0]["title"] == "Test Game"
    assert deals[0]["genre"] == "Action"
    assert deals[0]["original_price"] == 29.99
    assert deals[0]["sale_price"] == 10.00
    assert deals[0]["discount_percent"] == 75