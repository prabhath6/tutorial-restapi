from flask import Flask, jsonify, make_response, request, abort, Response
import model

app = Flask(__name__)
app.config.from_object(__name__)

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/api/v1/cities', methods=['GET', 'POST'])
@app.route('/api/v1/cities/<int:page>', methods=['GET'])
def city_endpoint(page=1):

    # get request
    if request.method == 'GET':
        per_page = 10
        query = model.City.select().paginate(page, per_page)
        data = [i.serialize for i in query]

        if data:
            res = jsonify({
                'cities': data,
                'meta': {'page': page, 'per_page': per_page, 'page_url': request.url}
                })
            res.status_code = 200
        else:
            output = {
            "error": "No results found. Check url again",
            "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res
    elif request.method == 'POST': # post request

        row = model.City.create(**request.json)
        query = model.City.select().where(
            model.City.name == row.name,
            model.City.district == row.district
            )
        data = [i.serialize for i in query]
        res = jsonify({
            'city': data,
            'meta': {'page_url': request.url}
            })
        res.status_code = 201
        return res

@app.route('/api/v1/cities/<string:country_code>', methods=['GET'])
@app.route('/api/v1/cities/<string:country_code>/<int:page>', methods=['GET'])
def city_country_endpoint(country_code, page=1):

    # get request
    if request.method == 'GET':
        per_page = 10
        query = model.City.select().where(model.City.countrycode == country_code).paginate(page, per_page)
        data = [i.serialize for i in query]

        if data:
            res = jsonify({
                'cities': data,
                'meta': {'page': page, 'per_page': per_page, 'page_url': request.url}
                })
            res.status_code = 200
        else:
            output = {
            "error": "No results found. Check url again",
            "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res


@app.route('/api/v1/cities/<string:country_code>/<string:city_name>', methods=['GET', 'DELETE', 'PUT'])
def city_country_city_endpoint(country_code, city_name):

    # get request
    if request.method == 'GET':
        per_page = 10
        query = model.City.select().where(
            model.City.countrycode == country_code,
            model.City.name == city_name
            )

        data = [i.serialize for i in query]

        if data:
            res = jsonify({
                'cities': data,
                'meta': {'page': 1, 'per_page': per_page, 'page_url': request.url}
                })
            res.status_code = 200
        else:
            output = {
            "error": "No results found. Check url again",
            "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

    elif request.method == "PUT":
        c = model.City.get(
            model.City.countrycode == country_code,
            model.City.name == city_name
            )

        if not c:
            abort(404)
        if not request.json:
            abort(400)

        if 'district' in request.json and type(request.json['district']) != str:
            abort(400)
        else:
            c.district = request.json['district']
        if 'population' in request.json and type(request.json['population']) is not int:
            abort(400)
        else:
            c.population = request.json['population']

        c.save()

        query = model.City.select().where(
            model.City.name == c.name,
            model.City.countrycode == c.countrycode
            )
        data = [i.serialize for i in query]
        res = jsonify({
            'city': data,
            'meta': {'page_url': request.url}
            })
        res.status_code = 200
        return res
    elif request.method == "DELETE":
        
        try:
            city = model.City.get(
                model.City.countrycode == country_code,
                model.City.name == city_name
                )
        except:
            city = None

        if city:
            city.delete_instance()
            res = jsonify({})
            res.status_code = 204
            return res
        else:
            res = jsonify({
                "Error": "The requested resource is no longer available at the server and no forwarding address is known.",
                "Status Code": 410,
                "URL" : request.url
                })
            res.status_code = 410
            return res


if __name__ == '__main__':
    app.run(debug=True)
