import Index from '@/views/external_sities/Index';
import New from '@/views/external_sities/New';

export default [
    {
        path: '/external_sities',
        name: 'external_sities',
        component: Index
    },
    {
        path: '/external_sities/new',
        name: 'external_sities_new',
        component: New
    },
    {
        path: '/external_sities/update',
        name: 'external_sities_update',
        component: New
    }
];
