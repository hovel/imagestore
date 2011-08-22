function split( val ) {
    return val.split( /,\s*/ );
}
function extractLast( term ) {
    return split( term ).pop();
}
function getAutocompleteParams(autocompleteUrl, multiply) {
    return {
    source: function(request, response){
        $.ajax({
            url: autocompleteUrl,
            data: {q: extractLast(request.term)},
            success: function(data) {
                response($.map(data, function(item) {
                    return {
                        label: item[1],
                        value: item[1]
                    };
                }));
            },
            dataType: "json"
        });
    },
    search: function() {
        // custom minLength
        var term = extractLast( this.value );
        if ( term.length < 2 ) {
            return false;
        }
    },
    focus: function() {
        // prevent value inserted on focus
        return false;
    },
    select: function( event, ui ) {
        if (multiply) {
            var terms = split(this.value);
            // remove the current input
            terms.pop();
            // add the selected item
            terms.push(ui.item.value);
            // add placeholder to get the comma-and-space at the end
            terms.push("");
            this.value = terms.join(", ");
        } else {
            this.value = ui.item.value;
        }
        return false;
    }
    }
}
function completeField(fieldId, autocompleteUrl, multiply){$(fieldId).autocomplete(getAutocompleteParams(autocompleteUrl, multiply));
}