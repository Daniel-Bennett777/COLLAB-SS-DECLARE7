import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create

class ShippingShipsView():
    def get_expanded(self, handler, pk):
        if pk != 0:
            sql = """
            SELECT s.id, s.name, s.hauler_id, h.name AS hauler_name
            FROM Ship s
            LEFT JOIN Hauler h ON s.hauler_id = h.id
            WHERE s.id = ?
            """
            query_results = db_get_single(sql, pk)

            if query_results:
                ship_data = dict(query_results)
                response = {
                    "id": ship_data["id"],
                    "name": ship_data["name"],
                    "hauler_id": ship_data["hauler_id"],
                    "hauler_name": ship_data["hauler_name"]
                }
                return handler.response(json.dumps(response), status.HTTP_200_SUCCESS.value)
            else:
                return "Error", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
        else:
            sql = """
            SELECT s.id, s.name, s.hauler_id, h.name AS hauler_name
            FROM Ship s
            LEFT JOIN Hauler h ON s.hauler_id = h.id
            """
            query_results = db_get_all(sql)

            expanded_ships = []

            for row in query_results:
                ship_data = dict(row)
                response = {
                    "id": ship_data["id"],
                    "name": ship_data["name"],
                    "hauler_id": ship_data["hauler_id"],
                    "hauler_name": ship_data["hauler_name"]
                }
                expanded_ships.append(response)

            if expanded_ships:
                return handler.response(json.dumps(expanded_ships), status.HTTP_200_SUCCESS.value)
            else:
                return handler.response("Error", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
    def get(self, handler, pk):
        if pk != 0:
            sql = "SELECT s.id, s.name, s.hauler_id FROM Ship s WHERE s.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_hauler = json.dumps(dict(query_results))

            return handler.response(serialized_hauler, status.HTTP_200_SUCCESS.value)
        else:

            sql = "SELECT s.id, s.name, s.hauler_id FROM Ship s"
            query_results = db_get_all(sql)
            haulers = [dict(row) for row in query_results]
            serialized_haulers = json.dumps(haulers)

            return handler.response(serialized_haulers, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Ship WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, ship_data, pk):
        sql = """
        UPDATE Ship
        SET
            name = ?,
            hauler_id = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (ship_data['name'], ship_data['hauler_id'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, ship_data):
        sql = """
        INSERT INTO Ship 
        VALUES(null, ?,?)
                
        """
                
        new_item = db_create(sql,(ship_data['name'], ship_data['hauler_id']))

        if new_item is not None:
            response_data =  {
                "id" : new_item,
                "name": ship_data ['name'],
                "hauler_id": ship_data ['hauler_id']

            }
        
        if new_item > 0:
            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("BAD REQUEST", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)
        