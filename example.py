# -*- coding: utf-8 -*-

#
# * Copyright (c) 2009-2020. Authors: Cytomine SCRLFS.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */


__author__ = "Hoyoux Renaud <renaud.hoyoux@cytomine.coop>"
__copyright__ = "Apache 2 license. Made by Cytomine SCRLFS, Belgium, https://www.cytomine.coop/"
__version__ = "1.0.0"

# This is a sample of a software that can be run by the Cytomine platform using the Cytomine Python client (https://github.com/cytomine/Cytomine-python-client).

import os
import sys
import logging
import shutil

import cytomine
from cytomine.models import ImageInstanceCollection, JobData


# -----------------------------------------------------------------------------------------------------------
def run(cyto_job, parameters):
    logging.info("----- test software v%s -----", __version__)
    logging.info("Entering run(cyto_job=%s, parameters=%s)", cyto_job, parameters)

    job = cyto_job.job
    project = cyto_job.project

    # I create a working directory that I will delete at the end of this run
    working_path = os.path.join("tmp", str(job.id))
    if not os.path.exists(working_path):
        logging.info("Creating working directory: %s", working_path)
        os.makedirs(working_path)

    try:
        test_int_parameter = int(parameters.my_integer_parameter)

        logging.info("Display test_int_parameter %s", test_int_parameter)

        # loop for images in the project 
        images = ImageInstanceCollection().fetch_with_filter("project", project.id)
        nb_images = len(images)
        logging.info("# images in project: %d", nb_images)

        #value between 0 and 100 that represent the progress bar displayed in the UI.
        progress = 0
        progress_delta = 100 / nb_images

        # Go through all images
        for (i, image) in enumerate(images):
            image_str = "{} ({}/{})".format(image.instanceFilename, i+1, nb_images)

            job.update(progress=progress, statusComment="Analyzing image {}...".format(image_str))
            logging.debug("Image id: %d width: %d height: %d resolution: %f magnification: %d filename: %s", image.id,
                          image.width, image.height, image.resolution, image.magnification, image.filename)



            logging.info("Finished processing image %s", image.instanceFilename)
            progress += progress_delta


        output_path = os.path.join(working_path, "output.txt")
        f= open(output_path,"w+")
        f.write("Input given was %d\r\n" % test_int_parameter)
        f.close() 

        #I save a file generated by this run into a "job data" that will be available in the UI. 
        job_data = JobData(job.id, "Generated File", "output.txt").save()
        job_data.upload(output_path)

    finally:
        logging.info("Deleting folder %s", working_path)
        shutil.rmtree(working_path, ignore_errors=True)


        logging.debug("Leaving run()")


if __name__ == "__main__":
    logging.debug("Command: %s", sys.argv)

    with cytomine.CytomineJob.from_cli(sys.argv) as cyto_job:
        run(cyto_job, cyto_job.parameters)


