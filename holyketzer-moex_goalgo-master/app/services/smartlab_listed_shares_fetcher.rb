class SmartlabListedSharesFetcher
  include Singleton

  MAX_RETRIES = 5
  WAIT_SLEEP = 0.05
  SCALE_COEFF = 1_000_000

  def fetch_for(ticker)
    url = "https://smart-lab.ru/q/#{ticker}/MSFO/number_of_shares/"
    response = open_url(url)
    body = response.body.to_s

    if response.status == 404 || body.include?("страницы не существует")
      puts "SmartLab 404 for number_of_shares #{ticker}"
      return nil
    end

    doc = Nokogiri::HTML(body)

    javascript_block = doc.at('script:contains("aQuarterData")').text
    diagram_var = javascript_block.split("\n").each_cons(2).find { |l1, l2| l1.include?("aQuarterData") }[1].strip

    data = diagram_var.sub("'diagram' :", "").chomp(",")
    data = JSON.parse(data)
    if data && data.size > 0
      puts "SmartLab number_of_shares #{ticker} #{data} quarters"

      quarters = data["categories"].map { |d| last_quarter_day(d) }
      values = data["data"].map { |s| s["y"]&.*(SCALE_COEFF) }

      line_header = doc.css("h2:contains('Число акций')")[0]
      table_headers = doc.css("th:contains('Число акций')")
      if values.any? && !(line_header.text.include?("млн") || table_headers.any? { |h| h.text.include?("млн") })
        raise "Unexpected count header for number_of_shares #{ticker}: #{line_header}"
      end

      number_of_shares = quarters.zip(values)
      number_of_shares
    else
      puts "SmartLab no data for number_of_shares #{ticker}"
      nil
    end
  end

  private

  def open_url(url)
    tries = 0
    begin
      sleep(WAIT_SLEEP)
      response = HTTP.get(url)
    rescue StandardError => e
      tries += 1
      if tries < MAX_RETRIES
        sleep(WAIT_SLEEP)
        retry
      else
        raise e
      end
    end
  end

  def last_quarter_day(date)
    year, quarter = date.split("Q")
    month = quarter.to_i * 3
    Date.civil(year.to_i, month, -1)
  end
end
