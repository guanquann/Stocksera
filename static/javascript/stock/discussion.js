function show_url_links(ticker_selected) {
    ticker_selected = ticker_selected.split(".")[0]
    document.querySelector("body").innerHTML += `
        <div class="more_discussion">
            <h2>View more discussions on Social Media:</h2>
            <div>-StockTwits: <a href="https://stocktwits.com/symbol/${ticker_selected}" target="_blank">https://stocktwits.com/symbol/${ticker_selected}</a></div>
            <div>-Twitter: <a href="https://twitter.com/search?q=$${ticker_selected}" target="_blank">https://twitter.com/search?q=$${ticker_selected}</a></div>
            <div>-Yahoo: <a href="https://finance.yahoo.com/quote/${ticker_selected}/community?p=${ticker_selected}" target="_blank">https://finance.yahoo.com/quote/${ticker_selected}/community?p=${ticker_selected}</a></div>
            <div>-Reddit: <a href="https://www.reddit.com/search/?q=$${ticker_selected}" target="_blank">https://www.reddit.com/search/?q=$${ticker_selected}</a></div>
        </div>
        <div class="scrollable_div">
            <iframe class="discussion_iframe" src="https://api.stocktwits.com/widgets/stream?&scrollbars=true&streaming=true&limit=100&title=${ticker_selected}
            %20Stock%20on%20StockTwits&width=1000&height=1100&symbol=${ticker_selected}&border_color=cecece&box_color=f5f5f5&header_text_color=000000&
            divider_color=cecece&stream_color=ffffff&divider_type=solid&link_color=4871a8&link_hover_color=4871a8&text_color=000000&
            time_color=999999">
            </iframe>
        </div>
    `
}
