import Index from '@/views/forms/Index';
import New from '@/views/forms/New';
import Detail from '@/views/forms/Detail';
import Edit from '@/views/forms/Edit';

export default [
    {
        path: '/forms.html',
        name: 'forms',
        component: Index
    },
    {
        path: '/forms/new',
        name: 'forms_new',
        component: New
    },
    {
        path: '/forms/:id/edit',
        name: 'forms_edit',
        component: Edit
    },
    {
        path: '/forms/:id',
        name: 'forms_detail',
        component: Detail
    }
];
