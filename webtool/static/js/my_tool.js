function setupDropZone(dropzone) {
    '设置拖入文件区域'
    const $tool_item = dropzone.closest('.tool-item');

    const $form = $tool_item.find('form');
    const $dropZone = $tool_item.find('[id^="drop-zone"]');

    const url = $form.attr('action');

    $dropZone.on('dragover', function(event) {
        event.preventDefault();
        $(this).addClass('highlight');
    });

    $dropZone.on('dragleave', function(event) {
        $(this).removeClass('highlight');
    });

    $dropZone.on('drop', function(event) {
        event.preventDefault();
        $(this).removeClass('highlight');

        const file = event.originalEvent.dataTransfer.files[0];
        const formData = new FormData();
        formData.append('file', file);

        const loading = $('<div class="loading"><span></span></div>');

        $(document).ajaxStart(function() {
            // 显示 loading div
            $form.append(loading)
            // 隐藏 form
            $form.hide();
        });

        // 当 AJAX 请求结束时
        $(document).ajaxStop(function() {
            // 显示 loading div
            $form.find('div.loading')
            // 隐藏 form
            $form.show();
        });

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            processData: false, // 不要让jQuery处理数据
            contentType: false, // 不要让jQuery设置content-type请求头
            xhrFields: {
                responseType: 'blob'
            },
            success: function(data, textStatus, jqXHR) {
                const url = window.URL.createObjectURL(new Blob([data]));
                const filename = jqXHR.getResponseHeader('X-Download-Filename');
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', decodeURIComponent(filename));
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                window.URL.revokeObjectURL(url);
                console.log('文件下载成功');
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('文件上传失败');
                console.log('Error: ' + errorThrown);
            }
        });
    });
}

$(document).ready(function() {
    $('[id^="drop-zone"]').each(function() {
        setupDropZone($(this));
    });
});