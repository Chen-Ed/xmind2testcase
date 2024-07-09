$(document).ready(function() {
    // DEMO input button click event
    $('#demo_input').click(function() {
        var complexJson = "{ \"example\": { \"key\": \"value\", \"list\": [\"item1\", \"item2\"] }, \"nested\": { \"sub\": \"data\" } }";
        $('#jsonInput').val(complexJson);
    });

    // Clear input button click event
    $('#clearInput').click(function() {
        $('#jsonInput').val('');
    });

    // Clear response button click event
    $('#clearResponse').click(function() {
        $('#response').val('');
    });

    $('#midlle-button_right2left').click(function() {
        $('#jsonInput').val($('#response').val());
    });

    // Copy response button click event
    $('#copyResponse').click(function() {
        var responseText = $('#response').val();
        navigator.clipboard.writeText(responseText)
            .then(() => {
                alert('Response copied to clipboard');
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
            });
    });

    // Select JSON button click event
    $('#select_json').click(function() {
        var json_path = $('#json_path').val();
        var jsonInput = $('#jsonInput').val();
        $.ajax({
            url: '/json_editor/select_json', // 替换为你的 Flask 视图函数路由
            type: 'POST',
            data: JSON.stringify({ json: jsonInput , json_path: json_path}),
            contentType: 'application/json',
            success: function(response) {
                $('#response').val(response); // 格式化并显示响应
            },
            error: function(error) {
                $('#response').val('Error: ' + error.responseText);
            }
        });
    });

    // Replace JSON button click event
    $('#replace_json').click(function() {
        var jsonInput = $('#jsonInput').val();
        var json_path = $('#json_path').val();
        var replace_value = $('#replace_value').val();
        $.ajax({
            url: '/json_editor/replace_json', // 替换为你的 Flask 视图函数路由
            type: 'POST',
            data: JSON.stringify({ json: jsonInput , json_path: json_path, replace_value: replace_value}),
            contentType: 'application/json',
            success: function(response) {
                $('#response').val(response); // 格式化并显示响应
            },
            error: function(error) {
                $('#response').val('Error: ' + error.responseText);
            }
        });
    });

    $('#formatButton').prop('disabled', true).css('background-color', '#cccccc');
//    $('#formatButton').on('click', function() {
//        let input = $('#jsonInput').val();
//        let output = $('#response').val();
//
//        try {
////            格式化输入框
//            let json = JSON.parse(input);
////            let formattedJson = JSON.stringify(json, null, 4);
////            $('#jsonInput').text(formattedJson);
//            $('#jsonInput').JSONView(json, { collapsed: true, nl2br: true, recursive_collapser: true,  key_marks: true, link_marks: true });
//            $('#json-renderer').jsonViewer(input, options);
//
////            格式化输出框
////            json = JSON.parse(output);
////            formattedJson = JSON.stringify(json, null, 4);
////            $('#response').text(formattedJson);
//            console.log('JSON 格式化成功');
//        } catch (error) {
//
//            console.log(error);
//
//        }
//    });


});
