class AlgopackFetcher
  include Singleton

  BASE_URL = "https://iss.moex.com/iss"

  def initialize
  end

  def fetch_shares(offset: 0, limit: 100)
    response = HTTP.get(
      [
        "#{BASE_URL}/securities.json?engine=stock",
        "market=shares",
        "type=common_share",
        "iss.meta=off",
        "start=#{offset}",
        "limit=#{limit}"
      ].join("&")
    )

    if response.status.success?
      securities = JSON.parse(response.body.to_s)["securities"]
      columns = securities["columns"]
      data = securities["data"]
      data.map do |row|
        Hash[columns.zip(row)]
      end
    else
      raise "Error fetching shares: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_share(secid)
    response = HTTP.get("#{BASE_URL}/securities/#{secid}.json?iss.meta=off")

    if response.status.success?
      body = JSON.parse(response.body.to_s)
      description = body["description"]
      columns = description["columns"]
      data = description["data"].map do |row|
        Hash[columns.zip(row)]
      end
      data.map { |row| Hash[row["name"].downcase, row["value"]] }
        .reduce({}, :merge)
        .merge("history_from" => parse_history_from(body))
    else
      raise "Error fetching share: #{response.status} #{response.body.to_s}"
    end
  end

  # TODO: remove? provide only latest cap
  def fetch_shares_cap_batch
    # https://iss.moex.com/iss/engines/stock/markets/shares/boardgroups/57/securities
    response = HTTP.get("#{BASE_URL}/engines/stock/markets/shares/boardgroups/57/securities.json?iss.meta=off")
    if response.status.success?
      body = JSON.parse(response.body.to_s)
      marketdata = body["marketdata"]
      columns = marketdata["columns"]
      data = marketdata["data"]
      data.map do |row|
        Hash[columns.zip(row)]
      end.map { |row| [row["SECID"], row["ISSUECAPITALIZATION"]] }.to_h
    else
      raise "Error fetching shares: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_shares_cap
    # https://iss.moex.com/iss/engines/stock/markets/shares/securities/OZON
    Share.where(cap: nil).map do |share|
      response = HTTP.get("#{BASE_URL}/engines/stock/markets/shares/securities/#{share.secid}.json?iss.meta=off")
      if response.status.success?
        body = JSON.parse(response.body.to_s)
        marketdata = body["marketdata"]
        columns = marketdata["columns"]

        cap = marketdata["data"]
          .map { |row| Hash[columns.zip(row)] }
          .map { |row| row["ISSUECAPITALIZATION"] }
          .compact
          .first

        if cap != nil
          puts "Fetched cap for #{share.secid}: #{cap}"
        end

        # share.update!(cap: cap)
      else
        raise "Error fetching share #{share.secid} cap: #{response.status} #{response.body.to_s}"
      end
    end
  end

  def fetch_history_prices(secid, from:, to: Date.today)
    # https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/SBER?from=1997-03-24&till=2023-12-01&marketprice_board=1&history.columns=TRADEDATE,WAPRICE,LOW,HIGH,OPEN,CLOSE,VOLUME&limit=1000
    response = HTTP.get(
      [
        "#{BASE_URL}/history/engines/stock/markets/shares/securities/#{secid}.json?from=#{from}",
        "till=#{to}",
        "marketprice_board=1",
        "history.columns=TRADEDATE,WAPRICE,LOW,HIGH,OPEN,CLOSE,VOLUME",
        "limit=1000"
      ].join("&")
    )

    if response.status.success?
      body = JSON.parse(response.body.to_s)
      history = body["history"]
      columns = history["columns"].map(&:downcase)
      data = history["data"]
      data.map do |row|
        Hash[columns.zip(row)]
      end
    else
      raise "Error fetching share #{secid} history prices: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_indexes(secids)
    # https://iss.moex.com/iss/engines/stock/markets/index/securities/
    response = HTTP.get("#{BASE_URL}/engines/stock/markets/index/securities.json?iss.meta=off")
    if response.status.success?
      body = JSON.parse(response.body.to_s)
      securities = body["securities"]
      columns = securities["columns"].map(&:downcase)
      data = securities["data"]
      data.map do |row|
        Hash[columns.zip(row)]
      end.select { |row| secids.include?(row["secid"]) }
    else
      raise "Error fetching indexes: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_indexes_history(secid, from:, to: Date.today)
    # https://iss.moex.com/iss/history/engines/stock/markets/index/securities/IMOEX?from=2023-03-24&till=2023-12-01&marketprice_board=1&history.columns=TRADEDATE,WAPRICE,LOW,HIGH,OPEN,CLOSE,VOLUME&limit=1000
    response = HTTP.get(
      [
        "#{BASE_URL}/history/engines/stock/markets/index/securities/#{secid}.json?from=#{from}",
        "till=#{to}",
        "marketprice_board=1",
        "history.columns=TRADEDATE,WAPRICE,LOW,HIGH,OPEN,CLOSE,VOLUME",
        "limit=1000"
      ].join("&")
    )

    if response.status.success?
      body = JSON.parse(response.body.to_s)
      history = body["history"]
      columns = history["columns"].map(&:downcase)
      data = history["data"]
      data.map do |row|
        Hash[columns.zip(row)]
      end
    else
      raise "Error fetching index #{secid} history prices: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_currencies
    # https://iss.moex.com/iss/engines/currency/markets/selt/boards/CETS/securities
    response = HTTP.get("#{BASE_URL}/engines/currency/markets/selt/boards/CETS/securities.json?iss.meta=off")
    if response.status.success?
      body = JSON.parse(response.body.to_s)
      securities = body["securities"]
      columns = securities["columns"].map(&:downcase)
      data = securities["data"]
      data
        .map { |row| Hash[columns.zip(row)] }
        .select { |row| row["secid"].end_with?("TOD") }
    else
      raise "Error fetching currencies: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_currencies_history(secid, from:, to: Date.today)
    # https://iss.moex.com/iss/history/engines/currency/markets/selt/boards/CETS/securities/USD000UTSTOM?from=2023-03-24&till=2023-12-01&history.columns=TRADEDATE,WAPRICE,LOW,HIGH,OPEN,CLOSE,VOLUME&limit=1000
    response = HTTP.get(
      [
        "#{BASE_URL}/history/engines/currency/markets/selt/boards/CETS/securities/#{secid}.json?from=#{from}",
        "till=#{to}",
        "history.columns=TRADEDATE,WAPRICE,LOW,HIGH,OPEN,CLOSE,VOLUME",
        "limit=1000"
      ].join("&")
    )

    if response.status.success?
      body = JSON.parse(response.body.to_s)
      history = body["history"]
      columns = history["columns"].map(&:downcase)
      data = history["data"]
      data.map do |row|
        Hash[columns.zip(row)]
      end
    else
      raise "Error fetching currency #{secid} history prices: #{response.status} #{response.body.to_s}"
    end
  end

  def fetch_listed_till(secid)
    response = HTTP.get("#{BASE_URL}/securities/#{secid}.json")

    if response.status.success?
      body = JSON.parse(response.body.to_s)
      boards = body["boards"]
      columns = boards["columns"]
      data = boards["data"]

      listed_till = data.map { |row| Hash[columns.zip(row)] }
        .select { |row| row["is_primary"] == 1 }
        .map { |row| row["listed_till"] }
        .first

      if listed_till
        listed_till = Date.parse(listed_till)
        (Date.today.to_time - listed_till.to_time) > 30.days ? listed_till : nil
      else
        nil
      end
    else
      raise "Error fetching share #{secid} listed till: #{response.status} #{response.body.to_s}"
    end
  end

  private

  def parse_history_from(body)
    boards = body["boards"]
    columns = boards["columns"]
    data = boards["data"]
    data.map { |row| Hash[columns.zip(row)] }
      .map { |row| row["history_from"] }
      .compact
      .min
  end

  def max_listed_till(body)

  end
end
