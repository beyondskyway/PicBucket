/*global Qiniu */
/*global plupload */
/*global FileProgress */
/*global hljs */

var col;
var isScroll = 0;

$(document).ready(function() {
	//vendor script
	$('#header')
	.css({ 'top':-50 })
	.delay(500)
	.animate({'top': 0}, 800);

	//blocksit define
	$(window).load( function() {
        var winWidth = $(window).width();
		var conWidth;
        if(winWidth < 750) {
            conWidth = winWidth;
            col = 2;
		} else if(winWidth < 1000) {
			conWidth = winWidth;
			col = 2;
		} else if(winWidth < 1250) {
			conWidth = 1000;
			col = 4;
		} else if(winWidth < 1500) {
			conWidth = 1250;
			col = 5;
		} else{
            conWidth = 1500;
			col = 6;
        }

        $('#contain').width(conWidth);
        $('#contain').BlocksIt({
            numOfCol: col,
            offsetX: 8,
            offsetY: 8,
            blockElement: '.grid'
        });
	});

	//window resize
	var currentWidth = 1500;
	$(window).resize(function() {
		var winWidth = $(window).width();
		var conWidth;
        if(winWidth < 750) {
            conWidth = winWidth;
            col = 2;
		} else if(winWidth < 1000) {
			conWidth = winWidth;
			col = 2;
		} else if(winWidth < 1250) {
			conWidth = 1000;
			col = 4;
		} else if(winWidth < 1500) {
			conWidth = 1250;
			col = 5;
		} else{
            conWidth = 1500;
			col = 6;
        }

		if(conWidth != currentWidth) {
			currentWidth = conWidth;
			$('#contain').width(conWidth);
			$('#contain').BlocksIt({
				numOfCol: col,
				offsetX: 8,
				offsetY: 8,
                blockElement: '.grid'
			});
		}
	});
});

// 渲染图片函数
var img_stop = function(){
    var height = 800;
    $('.img_load').each(function() {
		$(this).load(function(){
            if( $(this).height() > height){
                $(this).parent().parent().next().css('display', 'block');
            }
		});
    });
};

// 初始加载渲染图片
$(function(){
	img_stop();
});

var img_load = function(url, key) {
    var img = new Image();
    img.src = url;
    img.onload = load_img(img, key);
    function load_img(img, key){
        var height = img.height;
        if( height > 500){
            var str = 'div[data-key=' + key + ']';
            $(str).find('.stop').css('display', 'block');
        }
    }
};


$(window).scroll(function () {
    var clientHeight = $(window).height(),
        scrollTop = $(window).scrollTop(),
        scrollHeight = $(document).height();
    if (!isScroll && (scrollHeight - clientHeight - scrollTop < 500)) {
        isScroll = 1;
        $('#loading').show();
        // 获取最后一个块的key
        var key = $('.grid:last-child').data('key');
        // 请求数据
        $.ajax({
            url:"/picbed",
            type: "POST",
            data: { key: key}
        })
        .done(function(data){
            if(data === 'error') {
                alert('加载失败');
                location.reload(true);
                return false;
            }
            var pics = JSON.parse(data);
            //没有更多了
            if(jQuery.isEmptyObject(pics)){
                $('#load_img').hide();
                $('#load_text').text('没有更多了！');
                $('#contain').BlocksIt('reload');
                return false;
            }

            $.each(pics, function(index, val){
                var add =
                        "<div class='grid' data-key='" + this.key +"'>" +
                            "<div class='imgholder'>" +
                                "<a class='fopLink' data-key='"+ this.upkey + "'>" +
                                    "<img class='img_load' src='" + this.url +"' />" +
                                "</a>" +
                            "</div>" +
                            "<span class='stop'></span>" +
                            "<strong>"+ this.object +"</strong>" +
                            "<div class='description'>" +
                                "<p>"+ this.words +"</p>" +
                                "<div class='meta'>by " + this.author +"</div>" +
                            "</div>"+
                        "</div>";
                $("#contain").append(add);
                // 动态加载渲染图片
                img_stop();
            });
            $('#contain').BlocksIt('reload');
            // 第二次加载
            // 获取最后一个块的key
            key = $('.grid:last-child').data('key');
            // 请求数据
            $.ajax({
                url:"/picbed",
                type: "POST",
                data: { key: key}
            })
            .done(function(data){
                if(data === 'error') {
                    alert('加载失败');
                    location.reload(true);
                    return false;
                }
                var pics = JSON.parse(data);
                //没有更多了
                if(jQuery.isEmptyObject(pics)){
                    $('#load_img').hide();
                    $('#load_text').text('没有更多了！');
                    $('#contain').BlocksIt('reload');
                    return false;
                }
                $.each(pics, function(index, val){
                    var add =
                            "<div class='grid' data-key='" + this.key +"'>" +
                                "<div class='imgholder'>" +
                                    "<a class='fopLink' data-key='"+ this.upkey + "'>" +
                                        "<img class='img_load' src='" + this.url +"' />" +
                                    "</a>" +
                                "</div>" +
                                "<span class='stop'></span>" +
                                "<strong>"+ this.object +"</strong>" +
                                "<div class='description'>" +
                                    "<p>"+ this.words +"</p>" +
                                    "<div class='meta'>by " + this.author +"</div>" +
                                "</div>"+
                            "</div>";
                    $("#contain").append(add);
                    img_stop();
                });
                $('#loading').hide();
                $('#contain').BlocksIt('reload');
                isScroll = 0;
            });

        });
    }
});

$(function() {
    var uploader = Qiniu.uploader({
        runtimes: 'html5,flash,html4',
        browse_button: 'pickfiles',
        container: 'container',
        drop_element: 'container',
        max_file_size: '100mb',
        filters: {
            mime_types: [
                { title: "图片文件", extensions: "jpg,gif,png,bmp" }
            ],
            prevent_duplicates: true //不允许队列中存在重复文件
        },
        flash_swf_url: '/static/js/plupload/Moxie.swf',
        dragdrop: true,
        chunk_size: '4mb',
        uptoken_url: $('#uptoken_url').val(),
        domain: $('#domain').val(),
        // downtoken_url: '/downtoken',
        // unique_names: true,
        // save_key: true,
        // x_vars: {
        //     'id': '1234',
        //     'time': function(up, file) {
        //         var time = (new Date()).getTime();
        //         // do something with 'time'
        //         return time;
        //     },
        // },
        auto_start: true,
        init: {
            'FilesAdded': function(up, files) {
                $('table').show();
                $('#success').hide();
                plupload.each(files, function(file) {
                    var progress = new FileProgress(file, 'fsUploadProgress');
                    progress.setStatus("等待...");
                });
            },
            'BeforeUpload': function(up, file) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                if (up.runtime === 'html5' && chunk_size) {
                    progress.setChunkProgess(chunk_size);
                }
            },
            'UploadProgress': function(up, file) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                var chunk_size = plupload.parseSize(this.getOption('chunk_size'));
                progress.setProgress(file.percent + "%", up.total.bytesPerSec, chunk_size);

            },
            'UploadComplete': function() {
                $('#success').show();
            },
            'FileUploaded': function(up, file, info) {
                var progress = new FileProgress(file, 'fsUploadProgress');
                progress.setComplete(up, info);
                var res = $.parseJSON(info);
                // 请求后台存储
                var domain = up.getOption('domain');
                //url = domain + encodeURI(res.key);
                var link = domain + res.key;
                var key = res.key;
                $.ajax({
                    url:"/upQiniu",
                    type: "POST",
                    data: { key: key, url: link}
                })
                .done(function(data){
                    if(data === 'error') {
                        alert('上传失败');
                        location.reload(true);
                    }
                });
            },
            'Error': function(up, err, errTip) {
                $('table').show();
                var progress = new FileProgress(err.file, 'fsUploadProgress');
                progress.setError();
                progress.setStatus(errTip);
            }
            ,
            'Key': function(up, file) {
                //当前时间戳
                var key = new Date();
//                Y = key.getFullYear() + '-';
//                M = (key.getMonth()+1 < 10 ? '0'+(key.getMonth()+1) : key.getMonth()+1) + '-';
//                D = (key.getDate() < 10 ? '0'+key.getDate() : key.getDate()) + ' ';
//                h = (key.getHours() < 10 ? '0'+key.getHours() : key.getHours()) + ':';
//                m = (key.getMinutes() < 10 ? '0'+key.getMinutes() : key.getMinutes()) + ':';
//                s = (key.getSeconds() < 10 ? '0'+key.getSeconds() : key.getSeconds()) + '.';
//                ms = key.getMilliseconds();
//                return Y+M+D+h+m+s+ms;
                return key.getTime()
            }
        }
    });

    uploader.bind('FileUploaded', function() {
        console.log('hello man,a file is uploaded');
    });
    $('#container').on(
        'dragenter',
        function(e) {
            e.preventDefault();
            $('#container').addClass('draging');
            e.stopPropagation();
        }
    ).on('drop', function(e) {
        e.preventDefault();
        $('#container').removeClass('draging');
        e.stopPropagation();
    }).on('dragleave', function(e) {
        e.preventDefault();
        $('#container').removeClass('draging');
        e.stopPropagation();
    }).on('dragover', function(e) {
        e.preventDefault();
        $('#container').addClass('draging');
        e.stopPropagation();
    });



    $('#show_code').on('click', function() {
        $('#myModal-code').modal();
        $('pre code').each(function(i, e) {
            hljs.highlightBlock(e);
        });
    });


    $('body').on('click', 'table button.btn', function() {
        $(this).parents('tr').next().toggle();
    });


    var getRotate = function(url) {
        if (!url) {
            return 0;
        }
        var arr = url.split('/');
        for (var i = 0, len = arr.length; i < len; i++) {
            if (arr[i] === 'rotate') {
                return parseInt(arr[i + 1], 10);
            }
        }
        return 0;
    };

    $('#myModal-img .modal-body-footer').find('a').on('click', function() {
        var img = $('#myModal-img').find('.modal-body img');
        var key = img.data('key');
        var oldUrl = img.attr('src');
        var originHeight = parseInt(img.data('h'), 10);
        var fopArr = [];
        var rotate = getRotate(oldUrl);
        if (!$(this).hasClass('no-disable-click')) {
            $(this).addClass('disabled').siblings().removeClass('disabled');
            if ($(this).data('imagemogr') !== 'no-rotate') {
                fopArr.push({
                    'fop': 'imageMogr2',
                    'auto-orient': true,
                    'strip': true,
                    'rotate': rotate,
                    'format': 'png'
                });
            }
        } else {
            $(this).siblings().removeClass('disabled');
            var imageMogr = $(this).data('imagemogr');
            if (imageMogr === 'left') {
                rotate = rotate - 90 < 0 ? rotate + 270 : rotate - 90;
            } else if (imageMogr === 'right') {
                rotate = rotate + 90 > 360 ? rotate - 270 : rotate + 90;
            }
            fopArr.push({
                'fop': 'imageMogr2',
                'auto-orient': true,
                'strip': true,
                'rotate': rotate,
                'format': 'png'
            });
        }

        $('#myModal-img .modal-body-footer').find('a.disabled').each(function() {

            var watermark = $(this).data('watermark');
            var imageView = $(this).data('imageview');
            var imageMogr = $(this).data('imagemogr');

            if (watermark) {
                fopArr.push({
                    fop: 'watermark',
                    mode: 1,
                    image: 'http://7ximdq.com1.z0.glb.clouddn.com/1429546321312',
                    dissolve: 50,
                    gravity: watermark,
                    dx: 20,
                    dy: 20
                });
            }

            if (imageView) {
                var height;
                switch (imageView) {
                    case 'large':
                        height = originHeight;
                        break;
                    case 'middle':
                        height = originHeight * 0.5;
                        break;
                    case 'small':
                        height = originHeight * 0.1;
                        break;
                    default:
                        height = originHeight;
                        break;
                }
                fopArr.push({
                    fop: 'imageView2',
                    mode: 3,
                    h: parseInt(height, 10),
                    q: 100,
                    format: 'png'
                });
            }

            if (imageMogr === 'no-rotate') {
                fopArr.push({
                    'fop': 'imageMogr2',
                    'auto-orient': true,
                    'strip': true,
                    'rotate': 0,
                    'format': 'png'
                });
            }
        });

        var newUrl = Qiniu.pipeline(fopArr, key);

        var newImg = new Image();
        img.attr('src', '/static/img/loading.gif');
        newImg.onload = function() {
            img.attr('src', newUrl);
            img.parent('a').attr('href', newUrl);
        };
        newImg.src = newUrl;
        return false;
    });

});

function initImg(url, key, height) {
    $('#myModal-img').modal();
    var modalBody = $('#myModal-img').find('.modal-body');
    if (height <= 300) {
        $('#myModal-img').find('.text-warning').show();
    }
    var newImg = new Image();
    modalBody.find('img').attr('src', '/static/img/loading.gif').removeClass('show-img').addClass('loading-img');
    newImg.onload = function() {
        modalBody.find('img').attr('src', url).data('key', key).data('h', height);
//        modalBody.find('.modal-body-wrapper').find('a').attr('href', url);
        modalBody.find('.modal-body-wrapper').find('img').removeClass('loading-img').addClass('show-img');
    };
    newImg.src = url;
}
$('#contain').on('click', '.fopLink', function() {
    var height_space = 340;
    var key = $(this).data('key');
    var height = parseInt($(this).parents('.Wrapper').find('.origin-height').text(), 10);
    if (height > $(window).height() - height_space) {
        height = parseInt($(window).height() - height_space, 10);
    } else {
        height = parseInt(height, 10) || 300;
        //set a default height 300 for ie9-
    }
    var fopArr = [];
    fopArr.push({
        fop: 'imageView2',
        mode: 3,
        h: height,
        q: 100,
        format: 'png'
    });
//    fopArr.push({
//        fop: 'watermark',
//        mode: 1,
//        image: 'http://7ximdq.com1.z0.glb.clouddn.com/1429546321312',
//        dissolve: 100,
//        gravity: 'SouthEast',
//        dx: 100,
//        dy: 100
//    });
    var url = Qiniu.pipeline(fopArr, key);
    $('#myModal-img').on('hide.bs.modal', function() {
        $('#myModal-img').find('.btn-default').removeClass('disabled');
        $('#myModal-img').find('.text-warning').hide();
    }).on('show.bs.modal', function() {
        $('#myModal-img').find('.imageView').find('a:eq(0)').addClass('disabled');
        $('#myModal-img').find('.watermark').find('a:eq(4)').addClass('disabled');
        $('#myModal-img').find('.text-warning').hide();
    });

    initImg(url, key, height);

    return false;
});
