"use strict";
var KTDatatablesAdvancedColumnRendering = function () {

    var initTable1 = function () {
        var table = $('#kt_table_1');

        // begin first table
        table.DataTable({
            responsive: true,
            paging: true,
            columnDefs: [
                {
                    targets: 5,
                    render: function (data, type, full, meta) {
                        var status = {
                            // True: {'title': 'Kích hoạt', 'class': 'kt-badge--brand',},
                            False: {'title': 'Chưa kích hoạt', 'class': ' kt-badge--danger'},
                            // 3: {'title': 'Canceled', 'class': ' kt-badge--primary'},
                            True: {'title': 'Kích hoạt', 'class': ' kt-badge--success'},
                            // 5: {'title': 'Info', 'class': ' kt-badge--info'},
                            // 6: {'title': 'Danger', 'class': ' kt-badge--danger'},
                            // 7: {'title': 'Warning', 'class': ' kt-badge--warning'},
                        };
                        if (typeof status[data] === 'undefined') {
                            return data;
                        }
                        return '<span class="kt-badge ' + status[data].class + ' kt-badge--inline kt-badge--pill">' + status[data].title + '</span>';
                    },
                },
            ],
            createdRow: function (row, data, index) {
                var cell = $('td', row).eq(1);
                cell.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#716aca'
                })
                cell.html(KTUtil.numberString(data[1] + ' VND'));

                var cell1 = $('td', row).eq(2);
                cell1.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#f4516c'
                })
                cell1.html(KTUtil.numberString(data[2] + ' VND'));

                var cell2 = $('td', row).eq(3);
                cell2.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#5578eb'
                })
                cell2.html(KTUtil.numberString(data[3] + ' VND'));

                var cell3 = $('td', row).eq(4);
                if (data[4].replace(/[\$,]/g, '') * 1 > 10) {
                    cell3.addClass('highlight').css({
                        'font-weight': 'bold',
                        color: '#0abb87'
                    })
                } else {
                    cell3.addClass('highlight').css({
                        'font-weight': 'bold',
                        color: '#f4516c'
                    }).attr('title', 'Sắp hết hàng');
                }

                cell3.html(KTUtil.numberString(data[4]));
            },
            dom: 'Bfrtip',
            buttons: [
                'copy',
                {
                    extend: 'excel',
                    messageTop: 'The information in this table is copyright to Sirius Cybernetics Corp.'
                },
                {
                    extend: 'pdf',
                    messageBottom: null
                },
            ],
        });
    };
    var initTable2 = function () {
        var table = $('#kt_table_2');

        // begin first table
        table.DataTable({
            responsive: true,
            paging: true,
            columnDefs: [
                {
                    targets: 2,
                    render: function (data, type, full, meta) {
                        var status = {
                            // True: {'title': 'Kích hoạt', 'class': 'kt-badge--brand',},
                            False: {'title': 'Chưa kích hoạt', 'class': ' kt-badge--danger'},
                            // 3: {'title': 'Canceled', 'class': ' kt-badge--primary'},
                            True: {'title': 'Success', 'class': ' kt-badge--success'},
                            // 5: {'title': 'Info', 'class': ' kt-badge--info'},
                            // 6: {'title': 'Danger', 'class': ' kt-badge--danger'},
                            // 7: {'title': 'Warning', 'class': ' kt-badge--warning'},
                        };
                        if (typeof status[data] === 'undefined') {
                            return data;
                        }
                        return '<span class="kt-badge ' + status[data].class + ' kt-badge--inline kt-badge--pill">' + status[data].title + '</span>';
                    },
                },
            ],
            createdRow: function (row, data, index) {
                var cell = $('td', row).eq(1);
                cell.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#716aca'
                })
                cell.html(KTUtil.numberString(data[1] + ' VND'));
            },
            dom: 'Bfrtip',
            buttons: [
                'copy',
                {
                    extend: 'excel',
                    messageTop: 'The information in this table is copyright to Sirius Cybernetics Corp.'
                },
                {
                    extend: 'pdf',
                    messageBottom: null
                },
            ],
        });
    };
    var initTable3 = function () {
        var table = $('#kt_table_3');

        // begin first table
        table.DataTable({
            responsive: true,
            paging: true,
            order: [[0, 'desc']],
            columnDefs: [
                {
                    targets: 5,
                    title: 'Trạng Thái',
                    render: function (data, type, full, meta) {
                        var status = {
                            False: {'title': 'Chưa kích hoạt', 'class': ' kt-badge--danger'},
                            True: {'title': 'Kích hoạt', 'class': ' kt-badge--success'},
                        };
                        if (typeof status[data] === 'undefined') {
                            return data;
                        }
                        return '<span class="kt-badge ' + status[data].class + ' kt-badge--inline kt-badge--pill">' + status[data].title + '</span>';
                    },
                },
                {
                    targets: 6,
                    title: '',
                    orderable: false,
                    render: function (data, type, full, meta) {
                        return `
                        <a data-toggle="modal" data-target="#edit-bill" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Sửa">
                          <i class="la la-edit"></i>
                        </a>
                        <a data-toggle="modal" data-target="#exampleModal" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Xem">
                          <i class="far fa-eye"></i></a>
                         `;
                    },
                },
            ],
            createdRow: function (row, data, index) {
                var cell = $('td', row).eq(1);
                cell.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#716aca'
                })
                cell.html(KTUtil.numberString(data[1] + ' VND'));

                var cell1 = $('td', row).eq(2);
                cell1.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#f4516c'
                })
                cell1.html(KTUtil.numberString(data[2] + ' %'));
                //
                var cell2 = $('td', row).eq(4);
                cell2.addClass('highlight').css({
                    'font-weight': 'bold',
                    color: '#0abb87'
                })
            },
            dom: 'Bfrtip',
            buttons: [
                'copy',
                {
                    extend: 'excel',
                    messageTop: 'The information in this table is copyright to Sirius Cybernetics Corp.'
                },
                {
                    extend: 'pdf',
                    messageBottom: null
                },
            ],
            // ajax: 'bill/ajax-bill',
            // columns: [
            //     {data: "id"},
            //     {data: "Total_Money"},
            //     {data: "Sale"},
            //     {data: "Date_Create"},
            //     {data: "User__username"},
            //     {data: "Active"}
            // ]
        });
    };

    return {

        //main function to initiate the module
        init: function () {
            initTable3();
            initTable1();
            initTable2();
        },
        registerEvents: function () {
            $('tbody tr td.data-id').off('click').on('click', function () {
                var id = $(this).data('id');
                KTDatatablesAdvancedColumnRendering.loadDetailBill(id);
            });
            //edit bill
            $('tbody tr td.data-id i.la-edit').off('click').on('click', function () {
                var id = $(this).closest('td').data('id');
                KTDatatablesAdvancedColumnRendering.loadEditBill(id);
            })
            $('#submit-edit').off('click').on('click', function () {
                var id = $('#id').val();
                KTDatatablesAdvancedColumnRendering.updateBill(id);
            })
        },
        loadDetailBill: function (id) {
            $.ajax({
                url: 'bill/details-bill/' + id,
                data: {id: id},
                type: 'get',
                dataType: 'json',
                success: function (response) {
                    if (response.status == true) {
                        var html_product = '';
                        var product = response.product;
                        $.each(product, function (i, item) {
                            let formatter = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'VND'});
                            let price = formatter.format(item.Product__Price_New);
                            html_product += '<option data-id="' + item.Product_id + '" style="font-size: medium">'
                                + item.Product__title + '  x' + item.Quality + ' - ' + price +
                                '</option>';
                        });
                        var html_service = '';
                        var service = response.service;
                        $.each(service, function (i, item) {
                            let formatter = new Intl.NumberFormat('en-US', {style: 'currency', currency: 'VND'});
                            let price = formatter.format(item.Service__Price);
                            html_service += '<option data-id="' + item.Service_id + '" style="font-size: medium">'
                                + item.Service__title + '  x' + item.Quality + ' - ' + price +
                                '</option>';
                        });
                        $('#multiple-service').html(html_service);
                        $('#multiple-product').html(html_product);
                    }
                },
                error: function (err) {
                    alert('false')
                }
            })
        },
        loadEditBill: function (id) {
            $.ajax({
                url: 'bill/details/' + id,
                data: {id: id},
                type: 'get',
                dataType: 'json',
                success: function (response) {
                    if (response.status == true) {
                        $('#id').val(response.bill[0].id);
                        $('#total-price').val(response.bill[0].Total_Money);
                        $('#user-create').val(response.bill[0].User_id);
                        $('#sale').val(response.bill[0].Sale);
                        $('#select-bool').val(response.bill[0].Active.toString()).change();
                    }
                },
                error: function (err) {
                    console.log(err)
                }
            })
        },
        updateBill: function (id) {
            var status = $('#select-bool option:selected').val();
            var data = {
                status: status,
                id: id
            }
            $.ajax({
                url: 'bill/update-bill/' + id + '/',
                data: data,
                type: 'post',
                dataType: 'json',
                success: function () {
                    window.location.reload();
                },
                error: function (err) {
                    console.log(err)
                }
            })
        }
    };
}();

jQuery(document).ready(function () {
    KTDatatablesAdvancedColumnRendering.init();
    KTDatatablesAdvancedColumnRendering.registerEvents();


});