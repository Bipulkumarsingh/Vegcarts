from flask_restful import Resource
from src.response import Resp

resp = Resp()


class AboutUs(Resource):
    about_html = """
            <div style="width: 95%; margin: 0 auto; font-size: 2.4em;">
                <article style="background: white; padding: 20px; margin: 20px 0">
                    <section style="text-align: left; background: #fff; color: #1a71b8; padding: 10px">
                        <h2>About Us</h2>
                    </section>
                    <section style="margin: 0 0 20px;">
                        <p style="margin: 0 0 1em; font-family: Georgia, Times, serif; text-align:justify; text-justify:inter-word;">
                            Vegcarts is an e-commerce venture that provides fresh vegetable directly from farm to your doorstep. Vegcarts is established with a motto - 'Create value for our customer to build an ever-lasting relation. 
                            <br /><br />
                            Our efficient & bulk procurement, state-of-the-art storage & handling and unmatched logistics enable us to pass on the price and quality advantage to our customers.
                            <br /><br /> 
                            We firmly believe that ultimately it is the customer trust that creates profitable businesses. We bring highest quality products at the most honest, reasonable and competing price with unmatched convenience - savings on time and money!!!
                            <br /><br />
                            We shall continue to strive hard to innovate and discover efficient means to create value for our customers,employees and community.
                        </p>
                    </section>
                </article>		
            </div>
    """

    @staticmethod
    def post():
        return resp.http_405(data={"html": "Method not allowed"})

    def get(self):
        return resp.http_200(data={"html": self.about_html})
