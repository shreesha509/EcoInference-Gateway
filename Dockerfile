FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY gateway ${LAMBDA_TASK_ROOT}/gateway
COPY data ${LAMBDA_TASK_ROOT}/data
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/lambda_handler.py

CMD [ "lambda_handler.handler" ]