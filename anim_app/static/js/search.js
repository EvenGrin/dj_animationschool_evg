$(document).ready(function(){
    let search = $('#search')
    let search_clear = $('#search_clear')
    search_clear.on('click', function(){
        search.val('')
    })
    if (search.val()){
            console.log('21213')
            search_clear.removeClass('d-none')
        } else {
            search_clear.addClass('d-none')
        }
    search.on('input', function(){
        if (search.val()){
            console.log('21213')
            search_clear.removeClass('d-none')
        } else {
            search_clear.addClass('d-none')
        }
    })

})