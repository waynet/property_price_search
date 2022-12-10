var Manager;

require.config({
  paths: {
    core: 'solr/core',
    managers: 'solr/managers',
    widgets: 'solr/widgets',
    reuters: 'widgets'
  },
  urlArgs: "bust=" +  (new Date()).getTime()
});

(function ($) {

define([
  'managers/Manager.jquery',
  'core/ParameterStore',
  'reuters/ResultWidget',
  'reuters/TagcloudWidget',
  'reuters/CurrentSearchWidget.9',
  'reuters/AutocompleteWidget',
  'reuters/CountryCodeWidget',
  'widgets/jquery/PagerWidget'
], function () {
  $(function () {
    Manager = new AjaxSolr.Manager({
      solrUrl: 'http://127.0.0.1:8983/solr/map/'
    });
    Manager.addWidget(new AjaxSolr.ResultWidget({
      id: 'result',
      target: '#docs'
    }));
    Manager.addWidget(new AjaxSolr.PagerWidget({
      id: 'pager',
      target: '#pager',
      prevLabel: '&lt;',
      nextLabel: '&gt;',
      innerWindow: 1,
      renderHeader: function (perPage, offset, total) {
        $('#pager-header').html($('<span></span>').text('displaying ' + Math.min(total, offset + 1) + ' to ' + Math.min(total, offset + perPage) + ' of ' + total));
      }
    }));
    var fields = ['price_range', 'county', 'town', 'year'];
    for (var i = 0, l = fields.length; i < l; i++) {
      Manager.addWidget(new AjaxSolr.TagcloudWidget({
        id: fields[i],
        target: '#' + fields[i],
        field: fields[i]
      }));
    }
    Manager.addWidget(new AjaxSolr.CurrentSearchWidget({
      id: 'currentsearch',
      target: '#selection'
    }));
    Manager.addWidget(new AjaxSolr.AutocompleteWidget({
      id: 'text',
      target: '#search',
      fields: ['address', 'county', 'eircode']
    }));
    Manager.addWidget(new AjaxSolr.CountryCodeWidget({
      id: 'countries',
      target: '#countries',
      field: 'countryCodes'
    }));
    Manager.init();
    Manager.store.addByValue('q', '*:*');
    var params = {
      facet: true,
      'facet.field': ['price_range', 'county', 'town', 'year'],
      'facet.limit': 20,
      'facet.mincount': 1,
      'f.county.facet.limit': 20,
      'f.town.facet.limit': 20,
      'f.year.facet.limit': 15,
      'f.price_range.facet.limit': 10,
      // 'facet.date': 'date',
      // 'facet.date.start': '1987-02-26T00:00:00.000Z/DAY',
      // 'facet.date.end': '1987-10-20T00:00:00.000Z/DAY+1DAY',
      // 'facet.date.gap': '+1DAY',
      'json.nl': 'map'
    };
    for (var name in params) {
      Manager.store.addByValue(name, params[name]);
    }
    Manager.doRequest();
  });

  $.fn.showIf = function (condition) {
    if (condition) {
      return this.show();
    }
    else {
      return this.hide();
    }
  }
});

})(jQuery);
