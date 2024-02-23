# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.1].define(version: 2023_12_09_152251) do
  create_schema "_timescaledb_cache"
  create_schema "_timescaledb_catalog"
  create_schema "_timescaledb_config"
  create_schema "_timescaledb_functions"
  create_schema "_timescaledb_internal"
  create_schema "timescaledb_experimental"
  create_schema "timescaledb_information"

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"
  enable_extension "timescaledb"

  create_table "currencies", force: :cascade do |t|
    t.string "secid", null: false
    t.string "name", null: false
    t.string "short_name", null: false
    t.integer "lot_size", null: false
    t.integer "face_amount", default: 0, null: false
    t.string "face_currency", default: "RUB", null: false
    t.string "currency", null: false
    t.decimal "minstep", precision: 20, scale: 10, null: false
    t.string "status"
    t.string "remarks"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "currency_prices", force: :cascade do |t|
    t.bigint "currency_id", null: false
    t.string "secid", null: false
    t.date "date", null: false
    t.decimal "open", precision: 16, scale: 8
    t.decimal "close", precision: 16, scale: 8
    t.decimal "low", precision: 16, scale: 8
    t.decimal "high", precision: 16, scale: 8
    t.decimal "waprice", precision: 16, scale: 8
    t.index ["currency_id", "date"], name: "index_currency_prices_on_currency_id_and_date", unique: true
    t.index ["currency_id"], name: "index_currency_prices_on_currency_id"
    t.index ["secid"], name: "index_currency_prices_on_secid"
  end

  create_table "custom_index_items", force: :cascade do |t|
    t.bigint "custom_index_id", null: false
    t.bigint "share_id", null: false
    t.decimal "shares_count", precision: 24, scale: 8, null: false
    t.date "date", null: false
    t.decimal "weight", precision: 10, scale: 8, null: false
    t.index ["custom_index_id", "date"], name: "index_custom_index_items_on_custom_index_id_and_date"
    t.index ["custom_index_id"], name: "index_custom_index_items_on_custom_index_id"
    t.index ["share_id"], name: "index_custom_index_items_on_share_id"
  end

  create_table "custom_index_prices", force: :cascade do |t|
    t.bigint "custom_index_id", null: false
    t.date "date", null: false
    t.decimal "open", precision: 10, scale: 2, null: false
    t.decimal "close", precision: 10, scale: 2, null: false
    t.index ["custom_index_id"], name: "index_custom_index_prices_on_custom_index_id"
  end

  create_table "custom_indices", force: :cascade do |t|
    t.string "name", null: false
    t.json "settings", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.decimal "coeff_d", precision: 16, scale: 4
    t.string "status", default: "new", null: false
    t.integer "progress", default: 0, null: false
    t.string "error"
    t.bigint "user_id", null: false
    t.float "avg_mr"
    t.float "avg_yr"
    t.float "max_md"
    t.float "max_yd"
    t.float "rsd"
    t.float "sharp"
    t.index ["name"], name: "index_custom_indices_on_name", unique: true
    t.index ["user_id"], name: "index_custom_indices_on_user_id"
  end

  create_table "index_prices", force: :cascade do |t|
    t.bigint "shares_index_id", null: false
    t.string "secid", null: false
    t.date "date", null: false
    t.decimal "open", precision: 10, scale: 2
    t.decimal "close", precision: 10, scale: 2
    t.decimal "low", precision: 10, scale: 2
    t.decimal "high", precision: 10, scale: 2
    t.bigint "volume"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["secid"], name: "index_index_prices_on_secid"
    t.index ["shares_index_id", "date"], name: "index_index_prices_on_shares_index_id_and_date", unique: true
    t.index ["shares_index_id"], name: "index_index_prices_on_shares_index_id"
  end

  create_table "share_caps", force: :cascade do |t|
    t.bigint "share_id", null: false
    t.string "secid", null: false
    t.date "date", null: false
    t.bigint "cap", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["secid"], name: "index_share_caps_on_secid"
    t.index ["share_id", "date"], name: "index_share_caps_on_share_id_and_date", unique: true
    t.index ["share_id"], name: "index_share_caps_on_share_id"
  end

  create_table "share_macro_stats", force: :cascade do |t|
    t.bigint "share_id", null: false
    t.string "secid", null: false
    t.bigint "shares_count", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "cap"
    t.date "date", null: false
    t.index ["share_id"], name: "index_share_macro_stats_on_share_id"
  end

  create_table "share_prices", force: :cascade do |t|
    t.bigint "share_id", null: false
    t.string "secid", null: false
    t.date "date", null: false
    t.decimal "open", precision: 16, scale: 8
    t.decimal "close", precision: 16, scale: 8
    t.decimal "low", precision: 16, scale: 8
    t.decimal "high", precision: 16, scale: 8
    t.bigint "volume"
    t.decimal "waprice", precision: 16, scale: 8
    t.index ["secid"], name: "index_share_prices_on_secid"
    t.index ["share_id", "date"], name: "index_share_prices_on_share_id_and_date", unique: true
    t.index ["share_id"], name: "index_share_prices_on_share_id"
  end

  create_table "share_sectors", force: :cascade do |t|
    t.string "name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_share_sectors_on_name", unique: true
  end

  create_table "share_splits", force: :cascade do |t|
    t.bigint "share_id", null: false
    t.date "date"
    t.integer "before"
    t.integer "after"
    t.index ["share_id", "date"], name: "index_share_splits_on_share_id_and_date", unique: true
    t.index ["share_id"], name: "index_share_splits_on_share_id"
  end

  create_table "shares", force: :cascade do |t|
    t.string "secid", null: false
    t.string "name", null: false
    t.string "short_name", null: false
    t.string "isin", null: false
    t.bigint "issue_size", null: false
    t.integer "nominal_price_amount", default: 0, null: false
    t.string "nominal_price_currency", default: "RUB", null: false
    t.date "issue_date"
    t.integer "list_level"
    t.string "sec_type", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.date "history_from"
    t.integer "emmiter_id"
    t.money "cap", scale: 2
    t.integer "version", default: 0, null: false
    t.bigint "share_sector_id"
    t.date "listed_till"
    t.index ["isin"], name: "index_shares_on_isin"
    t.index ["secid"], name: "index_shares_on_secid", unique: true
  end

  create_table "shares_indices", force: :cascade do |t|
    t.string "secid", null: false
    t.string "name", null: false
    t.string "short_name", null: false
    t.string "currency", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["secid"], name: "index_shares_indices_on_secid", unique: true
  end

  create_table "users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.string "current_sign_in_ip"
    t.string "last_sign_in_ip"
    t.string "confirmation_token"
    t.datetime "confirmed_at"
    t.datetime "confirmation_sent_at"
    t.string "unconfirmed_email"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "provider", limit: 50, default: "", null: false
    t.string "uid", limit: 50, default: "", null: false
    t.index ["confirmation_token"], name: "index_users_on_confirmation_token", unique: true
    t.index ["email"], name: "index_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true
  end

end
