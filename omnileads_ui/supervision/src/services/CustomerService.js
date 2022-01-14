export default class CustomerService {
    getCustomersLarge() {
        return fetch('customer.json').then(res => res.json())
                .then(d => d.data);
    }
}