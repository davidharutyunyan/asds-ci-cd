import re
from io import StringIO

import boto3
import scrapy
import pandas as pd

from datetime import datetime
from scrapy_splash import SplashRequest
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

result = None
class RatesSpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://www.rate.am/hy/armenian-dram-exchange-rates/banks']
    res = None
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse_bank_names(self, response):
        bank_names = response.xpath(
            '//div[contains(@class, "relative  w-full h-12 md:h-10 flex items-center group-hover")]')

        names = []
        for name in bank_names:
            names.append(name.xpath('.//img/@alt').get())

        return pd.DataFrame(names, columns=['bank'])

    def parse_dates(self, response):
        dates = response.xpath('//div[contains(@class, "text-N60 z-2 whitespace-nowrap px-2 text-center hidden")]')

        current_dates = []
        for date in dates:
            extracted_list = date.xpath('.//text()').extract()

            cleaned_text = ''.join(extracted_list).replace(' ', '').replace(',', '')

            armenian_months = {
                'Հունվար': 'Jan', 'Փետրվար': 'Feb', 'Մարտ': 'Mar', 'Ապրիլ': 'Apr',
                'Մայիս': 'May', 'Հունիս': 'Jun', 'Հուլիս': 'Jul', 'Օգոստոս': 'Aug',
                'Սեպտ': 'Sep', 'Հոկտ': 'Oct', 'Նոյեմբեր': 'Nov', 'Դեկտ': 'Dec'
            }

            for arm_month, eng_month in armenian_months.items():
                if arm_month in cleaned_text:
                    cleaned_text = cleaned_text.replace(arm_month, eng_month)
            print(cleaned_text)
            current_year = datetime.now().year
            full_date_string = f"{current_year} {cleaned_text}"
            date_obj = datetime.strptime(full_date_string, '%Y %d%b%H:%M')

            current_dates.append(date_obj)

        df = pd.DataFrame({'date': current_dates})
        df = df.apply(pd.to_datetime, errors='coerce')

        return df

    def parse_values(self, response):
        rows = response.xpath(
            '//div[contains(@class, "flex items-center h-full justify-center relative gap-0.5") or contains(@class, "relative z-1 flex items-center h-full")]')
        all_values = []
        for i, row in enumerate(rows):
            text_values = row.xpath('.//text()').extract()
            text_values = [val.strip() for val in text_values if val.strip()]
            all_values.extend(text_values)

        chunked_data = [all_values[i:i + 6] for i in range(0, len(all_values), 6)]
        df = pd.DataFrame(chunked_data, columns=['usd_buy', 'usd_sell', 'eur_buy', 'eur_sell', 'rub_buy', 'rub_cell'])
        df = df.apply(pd.to_numeric, errors='coerce')

        return df

    def parse(self, response):
        global result
        banks = self.parse_bank_names(response)
        dates = self.parse_dates(response)

        values = self.parse_values(response)
        combined_df = pd.concat([banks, dates, values], axis=1)
        result =  combined_df
        print(self)

def run(event, context):
    current_date = datetime.now()

    formatted_date = current_date.strftime("%d-%m-%Y")
    object_name = f"{formatted_date}/scrapped.csv"
    bucket_name = 'asds-test-bucket'

    process = CrawlerProcess()
    process.crawl(RatesSpider)
    process.start()
    csv_buffer = StringIO()
    result.to_csv(csv_buffer, index=False)

    s3 = boto3.client('s3', region_name='eu-central-1')
    s3.put_object(Bucket=bucket_name, Key=object_name, Body=csv_buffer.getvalue())

