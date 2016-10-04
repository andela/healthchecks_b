$(function () {

    $('[data-toggle="tooltip"]').tooltip();

    $(".my-checks-name").click(function() {
        var $this = $(this);

        $("#update-name-form").attr("action", $this.data("url"));
        $("#update-name-input").val($this.data("name"));
        $("#update-tags-input").val($this.data("tags"));
        $('#update-name-modal').modal("show");
        $("#update-name-input").focus();

        return false;
    });

    function update_time(){
        var entries = [0,0,0,0,0,0,0,0,0,0,0,0]
            $period_years = $('#period_years').val()
            if($period_years!=''){
                entries[0]=$period_years
            }

            $period_months = $('#period_months').val()
            if($period_months!=''){
                entries[1]=$period_months
            }

            $period_weeks = $('#period_weeks').val()
            if($period_weeks=!''){
                entries[2]=$period_weeks
            }

            $period_days = $('#period_days').val()
            if($period_days!=''){
                entries[3]=$period_days
            }

            $period_hours = $('#period_hours').val()
            if($period_hours!=''){
                entries[4]=$period_hours
            }

            $period_minutes = $('#period_minutes').val()
            if($period_minutes != ''){
                entries[5]=$period_minutes
            }

            $grace_years = $('#grace_years').val()
            if($grace_years!=''){
                entries[6]=$grace_years
            }

            $grace_months = $('#grace_months').val()
            if($grace_months!=''){
                entries[7]=$grace_months
            }

            $grace_weeks = $('#grace_weeks').val()
            if($grace_weeks!=''){
                entries[8]=$grace_weeks
            }

            $grace_days = $('#grace_days').val()
            if($grace_days!=''){
                entries[9]=$grace_days
            }

            $grace_hours = $('#grace_hours').val()
            if($grace_hours!=''){
                entries[10]=$grace_hours
            }

            $grace_minutes = $('#grace_minutes').val()
            if($grace_minutes != ''){
                entries[11]=$grace_minutes
            }


            $p_years_to_sec = $period_years*365*86400
            $p_months_to_sec = $period_months*28*86400
            $p_weeks_to_sec = $period_weeks*7*86400
            $p_day_to_sec = $period_days*86400
            $p_hour_to_sec = $period_hours*3600
            $p_min_to_sec = $period_minutes*60
            $period_total = $p_years_to_sec+$p_months_to_sec+$p_weeks_to_sec+$p_day_to_sec+$p_hour_to_sec+$p_min_to_sec

            $g_years_to_sec = $grace_years*365*86400
            $g_months_to_sec = $grace_months*28*86400
            $g_weeks_to_sec = $grace_weeks*7*86400
            $g_day_to_sec = $grace_days*86400
            $g_hour_to_sec = $grace_hours*3600
            $g_min_to_sec = $grace_minutes*60
            $grace_total = $g_years_to_sec+$g_months_to_sec+$g_weeks_to_sec+$g_day_to_sec+$g_hour_to_sec+$g_min_to_sec
            

            if($period_total==0){
                $('#update-timeout-timeout').val(60)
            }else{
                $('#update-timeout-timeout').val($period_total)
            }
            
            if($grace_total==0){
                $('#update-timeout-grace').val(60)
            }else{
                $('#update-timeout-grace').val($grace_total)
            }
    }

    //Period Errors

    $('#period_years').bind('change keyup', function(){
        $val = $('#period_years').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>5){
            $('#period_years').css('border-color','red')
        }else{
            $('#period_years').css('border-color','')
            update_time()
        }
    })

    $('#period_months').bind('change keyup', function(){
        $val = $('#period_months').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>11){
            $('#period_months').css('border-color','red')
        }else{
            $('#period_months').css('border-color','')
            update_time()
        }
    })

    $('#period_weeks').bind('change keyup', function(){
        $val = $('#period_weeks').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>3){
            $('#period_weeks').css('border-color','red')
        }else{
            $('#period_weeks').css('border-color','')
            update_time()
        }
    })

    $('#period_days').bind('change keyup', function(){
        $val = $('#period_days').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>6){
            $('#period_days').css('border-color','red')
        }else{
            $('#period_days').css('border-color','')
            update_time()
        }
    })

    $('#period_hours').bind('change keyup', function(){
        $val = $('#period_hours').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>23){
            $('#period_hours').css('border-color','red')
        }else{
            $('#period_hours').css('border-color','')
            update_time()
        }
    })

    $('#period_minutes').bind('change keyup', function(){
        $val = $('#period_minutes').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>59){
            $('#period_minutes').css('border-color','red')
        }else{
            $('#period_minutes').css('border-color','')
            update_time()
        }
    })

        //Grace Period Errors

    $('#grace_years').bind('change keyup', function(){
        $val = $('#grace_years').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>5){
            $('#grace_years').css('border-color','red')
        }else{
            $('#grace_years').css('border-color','')
            update_time()
        }
    })

    $('#grace_months').bind('change keyup', function(){
        $val = $('#period_months').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>11){
            $('#grace_months').css('border-color','red')
        }else{
            $('#grace_months').css('border-color','')
            update_time()
        }
    })

    $('#grace_weeks').bind('change keyup', function(){
        $val = $('#period_weeks').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>3){
            $('#grace_weeks').css('border-color','red')
        }else{
            $('#grace_weeks').css('border-color','')
            update_time()
        }
    })

    $('#grace_days').bind('change keyup', function(){
        $val = $('#grace_days').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>6){
            $('#grace_days').css('border-color','red')
        }else{
            $('#grace_days').css('border-color','')
            update_time()
        }
    })

    $('#grace_hours').bind('change keyup', function(){
        $val = $('#grace_hours').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>23){
            $('#grace_hours').css('border-color','red')
        }else{
            $('#grace_hours').css('border-color','')
            update_time()
        }
    })

    $('#grace_minutes').bind('change keyup', function(){
        $val = $('#grace_minutes').val()
        if(isNaN($val) || $val<0 || $val.indexOf('e')>-1 || $val>59){
            $('#grace_minutes').css('border-color','red')
        }else{
            $('#grace_minutes').css('border-color','')
            update_time()
        }
    })

    $(".timeout-grace").click(function() {
        var $this = $(this);
        $("#update-timeout-form").attr("action", $this.data("url"));
        $('#update-timeout-modal').modal({"show":true, "backdrop":"static"});
        return false;
    });


    $(".check-menu-remove").click(function() {
        var $this = $(this);

        $("#remove-check-form").attr("action", $this.data("url"));
        $(".remove-check-name").text($this.data("name"));
        $('#remove-check-modal').modal("show");

        return false;
    });


    $("#my-checks-tags button").click(function() {
        // .active has not been updated yet by bootstrap code,
        // so cannot use it
        $(this).toggleClass('checked');

        // Make a list of currently checked tags:
        var checked = [];
        $("#my-checks-tags button.checked").each(function(index, el) {
            checked.push(el.textContent);
        });

        // No checked tags: show all
        if (checked.length == 0) {
            $("#checks-table tr.checks-row").show();
            $("#checks-list > li").show();
            return;
        }

        function applyFilters(index, element) {
            var tags = $(".my-checks-name", element).data("tags").split(" ");
            for (var i=0, tag; tag=checked[i]; i++) {
                if (tags.indexOf(tag) == -1) {
                    $(element).hide();
                    return;
                }
            }

            $(element).show();
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $("#checks-table tr.checks-row").each(applyFilters);
        // Mobile: for each list item, see if it needs to be shown or hidden
        $("#checks-list > li").each(applyFilters);

    });

    $(".pause-check").click(function(e) {
        var url = e.target.getAttribute("data-url");
        $("#pause-form").attr("action", url).submit();
        return false;
    });


    $(".usage-examples").click(function(e) {
        var a = e.target;
        var url = a.getAttribute("data-url");
        var email = a.getAttribute("data-email");

        $(".ex", "#show-usage-modal").text(url);
        $(".em", "#show-usage-modal").text(email);

        $("#show-usage-modal").modal("show");
        return false;
    });


    var clipboard = new Clipboard('button.copy-link');
    $("button.copy-link").mouseout(function(e) {
        setTimeout(function() {
            e.target.textContent = "copy";
        }, 300);
    })

    clipboard.on('success', function(e) {
        e.trigger.textContent = "copied!";
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        var text = e.trigger.getAttribute("data-clipboard-text");
        prompt("Press Ctrl+C to select:", text)
    });

});
