require 'csv'

class SectorLoader
  class << self
    def load
      csv_file = Rails.root.join("config/issues-by-sector-november-2023.csv")
      csv_data = CSV.read(csv_file, headers: true, col_sep: ";")

      sectors_by_name = {}
      csv_data.each do |row|
        sector_name = row["Sector (rus)"].strip()
        secid = row["Code"].strip()

        sectors_by_name[sector_name] ||= ShareSector.find_or_create_by!(name: sector_name)
        if (share = Share.find_by(secid: secid))
          share.update!(share_sector: sectors_by_name[sector_name])
        else
          puts "Share with secid `#{secid}` not found"
        end
      end
    end
  end
end
