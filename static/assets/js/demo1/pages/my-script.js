var BillConfig = {}
var BillControler = {
    init: function () {
        BillControler.registerEvents();

    },
    registerEvents: function () {
        //them san pham vao gio hang
        $('#kt_select2_1_validate').off('change').on('change', function () {
            var name = $('#kt_select2_1_validate option:selected').val();
            var price = $('#kt_select2_1_validate option:selected').data('price');
            var id = $('#kt_select2_1_validate option:selected').data('product');
            BillControler.displayProduct(name, price, id);
            BillControler.reformatPrice();
            BillControler.totalAll();
        });

        //them dich vu vao gio hang
        $('#select_service').off('change').on('change', function () {
            var name = $('#select_service option:selected').val();
            var price = $('#select_service option:selected').data('price');
            var id = $('#select_service option:selected').data('service');
            BillControler.displayService(name, price, id);
            BillControler.reformatPrice();
            BillControler.totalAll();
        });

        //xoa san pham hoac dich vu va update lai gia
        $('.bill-select').off('click').on('click', '.btn-label-danger', function () {
            $(this).closest('p').remove();
            BillControler.totalAll();
        });

        // cong tru update tong tien
        $('.bill-select').on('click', '.product .fa-minus', function () {
            var id_product = $(this).closest('p').data('product');
            var value_product = $('input[data-product=' + id_product + ']').val();//so luong
            var price_product = $('p[data-product=' + id_product + ']').data('price');//gia
            if (value_product <= 0) {
                value_product = 0;
            } else {
                value_product--;
            }
            $('input[data-product=' + id_product + ']').val(value_product);
            var total = parseInt($('#total').text(), 10);//tong tien cu
            var total_new = total;//tong tien moi
            total_new = price_product * value_product;
            $(this).closest('p').data('money', total_new);
            BillControler.reformatPrice();
            BillControler.totalAll();
        });
        $('.bill-select').on('click', '.service .fa-minus', function () {
            var id_service = $(this).closest('p').data('service');
            var value_service = $('input[data-service=' + id_service + ']').val();
            var price_service = $('p[data-service=' + id_service + ']').data('price');
            if (value_service <= 0) {
                value_service = 0;
            } else {
                value_service--;
            }
            $('input[data-service=' + id_service + ']').val(value_service);
            var total = parseInt($('#total').text(), 10);//tong tien cu
            var total_new = total;//tong tien moi
            total_new = price_service * value_service;
            $(this).closest('p').data('money', total_new);
            BillControler.totalAll();
        });
        $('.bill-select').on('click', '.product .fa-plus', function () {
            var id_product = $(this).closest('p').data('product');
            var value_product = $('input[data-product=' + id_product + ']').val();//so luong
            var price_product = $('p[data-product=' + id_product + ']').data('price');//gia
            value_product++;
            $('input[data-product=' + id_product + ']').val(value_product);

            var total = parseInt($('#total').text(), 10);//tong tien cu
            var total_new = total;//tong tien moi
            total_new = price_product * value_product;
            $(this).closest('p').data('money', total_new);
            BillControler.totalAll();
        })
        $('.bill-select').on('click', '.service .fa-plus', function () {
            var id_service = $(this).closest('p').data('service');
            var value_service = $('input[data-service=' + id_service + ']').val();
            var price_service = $('p[data-service=' + id_service + ']').data('price');
            value_service++;
            $('input[data-service=' + id_service + ']').val(value_service);

            var total = parseInt($('#total').text(), 10);//tong tien cu
            var total_new = total;//tong tien moi
            total_new = price_service * value_service;
            $(this).closest('p').data('money', total_new);
            BillControler.totalAll();
        })

        //them bill
        $('#submit').off('click').on('click', function () {
            BillControler.addBill()
        })


    },
    displayProduct: function (name, price, id) {
        var html = '<p class="product" data-money="' + price + '" data-price="' + price + '" data-product="' + id + '" style="margin-top: 1rem;">' + name + '<i style="margin-left: 1rem;cursor: pointer" class="fas fa-minus"></i>' +
            '<input data-product="' + id + '" value="1" type="text" class="form-control set-total"  style="height: 2rem;width: 4rem;display: inline-block;margin-left: 0.5rem;margin-right: 0.5rem" id="spinner">' +
            '<i class="fas fa-plus" style="cursor: pointer"></i>' +
            '<a data-name="' + name + '" style="float: right" href="javascript:;" data-repeater-delete="" class="btn-sm btn btn-label-danger btn-bold">' +
            '<i class="la la-trash-o" style="text-align: center"></i>' + 'Delete' + '</a>' + '</p>';
        $('.bill-select').append(html);
    },
    displayService: function (name, price, id) {
        var html = '<p class="service" data-money="' + price + '" data-price="' + price + '" data-service="' + id + '" style="margin-top: 1rem;">' + name + '<i style="margin-left: 1rem;cursor: pointer" class="fas fa-minus"></i>' +
            '<input data-service="' + id + '" value="1" type="text" class="form-control set-total"  style="height: 2rem;width: 4rem;display: inline-block;margin-left: 0.5rem;margin-right: 0.5rem" id="spinner">' +
            '<i class="fas fa-plus" style="cursor: pointer"></i>' +
            '<a data-name="' + name + '" style="float: right" href="javascript:;" data-repeater-delete="" class="btn-sm btn btn-label-danger btn-bold">' +
            '<i class="la la-trash-o" style="text-align: center"></i>' + 'Delete' + '</a>' + '</p>';
        $('.bill-select').append(html);
    },
    totalAdd: function (price, quality) {
        var total = parseInt($('#total').text(), 10);
        total += price * quality;
        $('#total').text(total);
        $('#total').attr('data-total', total);
    },
    totalAll: function () {
        var end = 0;
        $('.product,.service').each(function () {
            end += $(this).data('money');
        });
        // end = end - total + total_new;
        $('#total').text(end);
        BillControler.formatPrice()
    },
    formatPrice: function () {
        $('#total').priceFormat({
            prefix: 'VND ',
            thousandsSeparator: '.',
            centsLimit: 0
        })
    },
    reformatPrice: function () {
        var price = $('#total').text();
        var end = price.replace('VND ', '');
        $('#total').text(end);
    },
    addBill: function () {
        //tong tien
        var price = $('#total').text();
        price = price.replace(/\./g, '');
        price = price.replace('VND ', '');

        //json product
        var product = [];
        $('.product').each(function () {
            var id = $(this).data('product');
            item = {};
            item['id'] = $(this).data('product');
            item['quality'] = $('.product[data-product=' + id + '] input').val();
            product.push(item)
        })
        var jsonProduct = JSON.stringify(product);

        //json service
        var service = [];
        $('.service').each(function () {
            var id = $(this).data('service');
            item = {};
            item['id'] = $(this).data('service');
            item['quality'] = $('.service[data-service=' + id + '] input').val();
            service.push(item)
        })
        var jsonService = JSON.stringify(service);

        //data
        var data = {
            total: price,
            product: jsonProduct,
            service: jsonService,
            // csrfmiddlewaretoken:window.CSRF_TOKEN
        };
        $.ajax({
            url: $('#submit').data('url'),
            data: data,
            type: 'POST',
            dataType: 'json',
            success: function (data) {
                if (data.status == true) {
                    window.location.reload();
                    // $('#kt_table_3 tbody').html(data.bill);

                }
            },
            error: function (err) {
                console.log(err);
            }
        })
    },


}
BillControler.init()