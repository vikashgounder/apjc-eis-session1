// use below 3 lines of import when doing local development
// comment/remove below 3 lines when loading on AppD Synthetic API Monitoring
import client from 'got';
import { DOMParser } from '@xmldom/xmldom';
import assert from 'assert';

// uncomment below 2 lines when loading this script on AppD API Monitoring
//const assert = require("assert");
//const { DOMParser } = require('@xmldom/xmldom');

(async () => {
    try {
        const response = await client.get("http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso/FullCountryInfoAllCountries");
        
        assert.equal(response.statusCode, 200, "Expected a successful status code of 200");
        assert.equal(response.statusMessage, "OK", "Expected status message to be 'OK'");

        const parser = new DOMParser().parseFromString(response.body, 'text/xml');
        
        // Count the number of phone codes using modern array methods
        const phoneCodes = parser.getElementsByTagName("sPhoneCode");
        console.log(`Total count of Codes: ${phoneCodes.length}`);
        assert.equal(phoneCodes.length, 246, `Expected 246 phone codes, but found ${phoneCodes.length}`);
        
        // Find the capital city for a specific country using XPath
        const andorraCapital = parser.getElementsByTagName("sCapitalCity")[0].textContent;
        console.log(`Capital of Andorra: ${andorraCapital}`);
        assert.strictEqual(andorraCapital, "Andorra La Ville", "Expected capital of Andorra to be 'Andorra La Ville'");
        
        // Find the capital of Zimbabwe
        const zimbabweCapital = parser.getElementsByTagName("sCapitalCity")[245].textContent;
        console.log(`Capital of Zimbabwe: ${zimbabweCapital}`);
        assert.strictEqual(zimbabweCapital, "Harare", "Expected capital of Zimbabwe to be 'Harare'");

    } catch (error) {
        console.error("An error occurred during the script execution:", error.message);
        throw error; // Re-throw the error to fail the synthetic monitor
    }
})();