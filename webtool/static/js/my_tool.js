function setupDropZone(dropZoneId, url) {
    const $dropZone = $('#' + dropZoneId);

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
                const filename = jqXHR.getResponseHeader('Content-Disposition').split('filename=')[1];
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
        const dropZoneId = this.id;
        const url = $(this).closest('form').attr('action');
        setupDropZone(dropZoneId, url);
    });
});