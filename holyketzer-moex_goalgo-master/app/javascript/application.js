// Configure your import map in config/importmap.rb. Read more: https://github.com/rails/importmap-rails
import "@hotwired/turbo-rails"
import "controllers"

document.addEventListener('turbo:load', function() {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  $('.multiple-select-field').select2({
    theme: "bootstrap-5",
    width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
    placeholder: $(this).data('placeholder'),
    closeOnSelect: false,
  });

  // Send selected filter to server and update shares filtered count
  $('#filter_listing, #filter_sector, #filter_tickers').on('change', function() {
    $.ajax({
      url: "/custom_indexes/filter_check",
      type: "POST",
      data: {
        listing: $('#filter_listing').val(),
        sectors: $('#filter_sector').val(),
        tickers: $('#filter_tickers').val()
      }
    }).done(function(data) {
      if (data["count"] >= 0) {
        $('#filtered-count').html(data["count"]);
        $('#filtered-count').removeClass('text-danger text-warning text-success text-predanger');
        if (data["count"] < 5) {
          $('#filtered-count').addClass('text-danger');
        } else if (data["count"] < 20) {
          $('#filtered-count').addClass('text-predanger');
        } else if (data["count"] < 50) {
          $('#filtered-count').addClass('text-warning');
        } else {
          $('#filtered-count').addClass('text-success');
        }
      }

      if (data["count"] > 0) {
        $('#create-index').removeClass('disabled');
      } else {
        $('#create-index').addClass('disabled');
      }
    });
  });

  // On each change update index name
  $('#review_period, #filter_listing, #filter_sector, #filter_tickers, #selection_topcap, #topcap_count, #selection_momentum, #momentum_days, #weighing').on('change', function() {
    if (document.index_name_changed_by_user) {
      return;
    }

    var name = "";

    let append = function(str) {
      if (name.length > 0) {
        name += " ";
      }
      name += str;
    }

    let stringToHash = function(string) {
      let hash = 0;
      if (string.length == 0) return hash;
      for (var i = 0; i < string.length; i++) {
        let char = string.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
      }
      return hash;
    }

    let mod = function(x, n) {
      return ((x % n) + n) % n;
    };

    if ($('#weighing').val() == "equal") {
      append("Равновзвешенный");
    }

    if ($('#selection_topcap').prop("checked")) {
      append("Топ" + $('#topcap_count').val());
    } else {
      append("Моментум" + $('#momentum_days').val());
    }

    let listings = $('#filter_listing').val();
    if (listings.length > 0) {
      append("Эшелон" + listings.join("+"));
    }

    let sectors = $("#filter_sector").select2("data").map(function (x) { return x.text });
    if (sectors.length > 0) {
      append(sectors.join(" "));
    }

    let tickers = $('#filter_tickers').val();
    if (tickers.length > 0) {
      tickers.sort();
      append("Выборка №" + mod(stringToHash(tickers.join(" ")), 500));
    }

    let review_period = $('#review_period').val();
    if (review_period == "quarterly") {
      append("q");
    } else {
      append("y");
    }

    $('#index_name').val(name).trigger('change');
    // set focus to index name field
    $('#index_name').focus();
    // the unfocus it
    $('#index_name').blur();
  });

  // identify any key press on index_name field
  $('#index_name').on('keyup', function() {
    document.index_name_changed_by_user = true;
  });
});
