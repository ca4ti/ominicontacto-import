export default {
    option: 'گزینه | گزینه ها',
    name: 'نام',
    agent: 'عامل | عوامل',
    campaign: 'زنگ | زنگ ها',
    group: 'گروه | گروه ها',
    campaign_info: 'زنگ: {name}',
    penalty: 'هزینه جریمه',
    agents_campaign: 'عوامل کمپین',
    clean_object: 'پاک کردن{object}',
    find_by: 'جستجو بر اساس {field}...',
    select_a: 'a را انتخاب کنید {field}',
    agent_campaign: {
        name: 'نام',
        username: 'Username',
        sip: 'ID SIP',
        penalty: 'هزینه جریمه'
    },
    sweet_alert: {
        title: {
            success: 'عملیات موفقیت آمیز!',
            error: 'عملیات اشتباه!',
            warning: 'هشدار!',
            sure: 'مطمئنی؟',
        },
        icons: {
            success: 'success',
            error: 'error',
            warning: 'warning',
            info: 'info',
        }
    },
    actions: {
        new: 'جدید',
        add: 'اضافه کردن',
        delete: 'حذف',
        create: 'خلق كردن',
        clean: 'پاک کردن',
        edit: 'ویرایش کنید',
        update: 'به روز رسانی',
        show: 'دیدن | نمایش دهید',
        save: 'نگاه داشتن',
        find: 'جستجو کنید',
        exit: 'برو بیرون',
        close: 'بستن',
        download: 'دانلود',
        back_to: 'بازگشت به {type}',
        yes: 'آره',
        no: 'خیر',
        cancel: 'لغو کنید',
        clean_filter: 'فیلتر تمیز',
        cancelled: 'عملیات لغو شد',
    },
    pages: {
        dashboard_home_page: {
            active_campaign_by_type: 'Campañas {type} Activas',
            campaigns: {
                inbound: 'شروع کننده ها',
                dialer: 'Dialer',
                manual: 'راهنماها',
                preview: 'Preview'
            },
            agent_status: 'وضعیت نماینده',
            call_sumary: 'خلاصه تماس'
        },
        add_agents_to_campaign: {
            delete_agent: 'عامل را حذف کنید',
            empty_agents: 'هیچ عاملی پیدا نشد',
            load_info: 'در حال بارگیری اطلاعات',
            already_agent_in_campaign: 'این نماینده در حال حاضر در کمپین است',
            already_agents_in_campaign: 'عوامل زیر قبلاً در کمپین حضور داشتند: ( {agents} )',
            not_select_type: 'شما a را انتخاب نکردید {type}',
            select_type: 'انتخاب کنید {type}',
            how_to_edit_penalty: 'برای تغییر مجازات، ستون را انتخاب کنید',
            group_added_success: 'گروه با موفقیت اضافه شد',
            agent_added_success: 'عامل با موفقیت اضافه شد',
            agents_added_success: 'عوامل با موفقیت ارتقا یافتند',
            agents_added_error: 'خطا در به‌روزرسانی عوامل',
            agent_deleted_success: 'نماینده با موفقیت حذف شد',
            agents_not_save: 'عوامل ذخیره نشدند',
            empty_campaign_notice: 'کارگزاران کمپین تمام خواهد شد',
            penalty_updated_success: 'پنالتی با موفقیت به روز شد',
        }
    }
}
