class Share < ApplicationRecord
  NO_ISIN = "NO_ISIN"
  COMMON_SHARE = "common_share"
  PREFERRED_SHARE = "preferred_share"
  DEPOSITARY_RECEIPT = "depositary_receipt"
  SHARE_TYPES = [COMMON_SHARE, PREFERRED_SHARE, DEPOSITARY_RECEIPT].freeze

  monetize :nominal_price_amount
  belongs_to :share_sector, optional: true
end
