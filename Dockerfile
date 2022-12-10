FROM python:3.8-alpine

# Create the app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . /usr/src/app

# Run the app
CMD ["python", "osp_bot.py"]