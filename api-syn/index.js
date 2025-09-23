// use below 3 lines of import when doing local development
// comment/remove below 3 lines when loading on AppD Synthetic API Monitoring
import client from 'got';
import { DOMParser } from '@xmldom/xmldom';
import assert from 'assert';

// uncomment below 2 lines when loading this script on AppD API Monitoring
//const assert = require("assert");
//const { DOMParser } = require('@xmldom/xmldom');
 
(async () => {
    var response = await client.get("https://www.w3schools.com/xml/simple.xml");
    assert.equal(response.statusCode, 200);
    assert.equal(response.statusMessage, "OK");
 
    var parser = new DOMParser().parseFromString(response.body);
    var get_name = parser.getElementsByTagName("calories")[0].childNodes[0].nodeValue;
    console.log(get_name);
    assert.equal(get_name, 650);

    var get_stores = parser.getElementsByTagName("calories");
    for (var store_count = 0; store_count < get_stores.length;) {
        //var get_store = get_stores[store_count].nodeValue;
        store_count++;
    }
    console.log(store_count);
    assert.equal(store_count, 5);
 
})();