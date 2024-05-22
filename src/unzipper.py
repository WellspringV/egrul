import zipfile
import json


def smart_unzip(json_archive):
    with zipfile.ZipFile(json_archive, 'r') as zip_ref:
        filenames = zip_ref.namelist()
        for file in filenames:
            yield zip_ref.extract(file)

# def read_and_drop(json):

        # bar = IncrementalBar('Handling', max=len(filenames))

        # for file in filenames:
        #     try:
        #         bar.next()
        #         zip_ref.extract(filename)
        #         res = complex_filter(filename, first_filter_param, second_filter_param)
        #     except Exception as e:   
        #         logging.error(f'Error {type(e).__name__} on filename {filename}', exc_info=e)
        #     else:
        #         if res:
        #             write_to_default_db(res)
        #     finally:       
        #         if os.path.exists(filename):
        #             os.remove(filename)
        # bar.finish()





