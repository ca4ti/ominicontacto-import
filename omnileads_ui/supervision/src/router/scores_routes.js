import Index from '@/views/scores/Index';
import New from '@/views/scores/New';
import Edit from '@/views/scores/Edit';

export default [
    {
        path: '/scores.html',
        name: 'scores',
        component: Index
    },
    {
        path: '/scores/new',
        name: 'scores_new',
        component: New
    },
    {
        path: '/scores/:id/update',
        name: 'scores_update',
        component: Edit
    }
];
