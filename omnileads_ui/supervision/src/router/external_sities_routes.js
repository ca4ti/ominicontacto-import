import Index from '@/views/external_sities/Index';
import New from '@/views/external_sities/New';
import Edit from '@/views/external_sities/Edit';

export default [
    {
        path: '/external_sities.html',
        name: 'external_sities',
        component: Index
    },
    {
        path: '/external_sities/new',
        name: 'external_sities_new',
        component: New
    },
    {
        path: '/external_sities/:id/update',
        name: 'external_sities_update',
        component: Edit
    }
];
