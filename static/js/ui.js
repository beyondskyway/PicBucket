/*global plupload */
/*global qiniu */
function FileProgress(file, targetID) {
    this.fileProgressID = file.id;
    this.file = file;

    this.opacity = 100;
    this.height = 0;
    this.fileProgressWrapper = $('#' + this.fileProgressID);
    if (!this.fileProgressWrapper.length) {
        var file_Size = plupload.formatSize(file.size).toUpperCase();
        var title = file.name + '(' + file_Size + ')';
        var add =
                '<span class="filename original" style="float: left;">'+ title + '</span>' +
                    '<div class="progress">' +
                        '<div class="percent"></div>' +
                        '<div class="bar" style="width: 0%;">' +
                    '</div>' +
                '</div>';
        this.fileProgressWrapper = $('<div></div>');
        var Wrappeer = this.fileProgressWrapper;
        Wrappeer.attr('id', this.fileProgressID).addClass('file-list progressContainer');

        Wrappeer.append(add);

        $('#' + targetID).append(Wrappeer);

    } else {
        this.reset();
    }

    this.height = this.fileProgressWrapper.offset().top;
    this.setTimer(null);
}

FileProgress.prototype.setTimer = function(timer) {
    this.fileProgressWrapper.FP_TIMER = timer;
};

FileProgress.prototype.getTimer = function(timer) {
    return this.fileProgressWrapper.FP_TIMER || null;
};

FileProgress.prototype.reset = function() {
    this.fileProgressWrapper.attr('class', "file-list progressContainer");
    this.appear();
};

// 查看分块上传进度
FileProgress.prototype.setChunkProgess = function(chunk_size) {
    return false;
};

// 设置进度
FileProgress.prototype.setProgress = function(percentage, speed, chunk_size) {
    this.fileProgressWrapper.attr('class', " file-list progressContainer red");

    var file = this.file;
    var uploaded = file.loaded;

    var size = plupload.formatSize(uploaded).toUpperCase();

    percentage = parseInt(percentage, 10);
    if (file.status !== plupload.DONE && percentage === 100) {
        percentage = 99;
    }

    this.fileProgressWrapper.find('.percent').text(percentage + '%');
    this.fileProgressWrapper.find('.bar').css('width', percentage + '%');

    this.appear();
};

// 完成上传
FileProgress.prototype.setComplete = function(up, info) {
    var filename = this.fileProgressWrapper.find('.filename').text();
    this.fileProgressWrapper.find('.filename').remove();
    this.fileProgressWrapper.find('.progress').remove();

    var res = $.parseJSON(info);
    var url;
    if (res.url) {
        url = res.url;
        var img_info =
            '<div class="attachment-meta new">' +
                '<span class="title">'+ filename +'</span>' +
                '<a class="remove-attachment" data-id="'+ res.key +'">删除</a>' +
            '</div>';
    } else {
        var domain = up.getOption('domain');
        url = domain + encodeURI(res.key);
        var img_info =
            '<div class="attachment-meta new">' +
                '<span class="title">'+ filename +'</span>' +
                '<a class="remove-attachment" data-id="'+ res.key +'">删除</a>' +
            '</div>';
    }
    var showImg = $('<img class="thumb" src="/static/img/img-loading.png"/>');
    var imageView = '?imageView2/1/w/100/h/100';

    var img = new Image();

    if (!/imageView/.test(url)) {
        url += imageView
    }

    $(img).attr('src', url);

    // 加载完成
    $(img).on('load', function() {
        showImg.attr('src', url);
    }).on('error', function() {
        showImg.attr('src', '/static/img/img-error.png');
    });

    this.fileProgressWrapper.append(showImg);
    this.fileProgressWrapper.append(img_info);
};

// 出错处理
FileProgress.prototype.setError = function() {

};

// 取消上传？
FileProgress.prototype.setCancelled = function(manual) {
    var progressContainer = 'file-list progressContainer';
    if (!manual) {
        progressContainer += ' red';
    }
    this.fileProgressWrapper.attr('class', progressContainer);
};

// 设置上传状态
FileProgress.prototype.setStatus = function(status, isUploading) {
    if (!isUploading) {
        this.fileProgressWrapper.find('.status').text(status).attr('class', 'status text-left');
    }
};

// 显示进度条？
FileProgress.prototype.appear = function() {
    if (this.getTimer() !== null) {
        clearTimeout(this.getTimer());
        this.setTimer(null);
    }

    if (this.fileProgressWrapper[0].filters) {
        try {
            this.fileProgressWrapper[0].filters.item("DXImageTransform.Microsoft.Alpha").opacity = 100;
        } catch (e) {
            // If it is not set initially, the browser will throw an error.  This will set it if it is not set yet.
            this.fileProgressWrapper.css('filter', "progid:DXImageTransform.Microsoft.Alpha(opacity=100)");
        }
    } else {
        this.fileProgressWrapper.css('opacity', 1);
    }

    this.fileProgressWrapper.css('height', '');

    this.height = this.fileProgressWrapper.offset().top;
    this.opacity = 100;
    this.fileProgressWrapper.show();

};
