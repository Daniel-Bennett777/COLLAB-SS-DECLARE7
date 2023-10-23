import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create

class HaulerView():

    def get_expanded(self, handler, pk):
        sql = """
            SELECT h.id, h.name, h.dock_id, d.location AS dock_location, d.capacity AS dock_capacity
            FROM Hauler h
            LEFT JOIN Dock d ON h.dock_id = d.id
            WHERE h.id = ?
            """
        query_results = db_get_single(sql, pk)

        if query_results:
            hauler_data = dict(query_results)
            dock_data = {
                "id": hauler_data["dock_id"],
                "location": hauler_data["dock_location"],
                "capacity": hauler_data["dock_capacity"]
            }
            response = {
                "id": hauler_data["id"],
                "name": hauler_data["name"],
                "dock_id": hauler_data["dock_id"],
                "dock": dock_data
            }
            return handler.response(json.dumps(response), status.HTTP_200_SUCCESS.value)
        else:
            return "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value

    def get(self, handler, pk):
        if pk != 0:
            sql = "SELECT h.id, h.name, h.dock_id FROM Hauler h WHERE h.id = ?"
            query_results = db_get_single(sql, pk)
            serialized_hauler = json.dumps(dict(query_results))

            return handler.response(serialized_hauler, status.HTTP_200_SUCCESS.value)
        else:

            sql = "SELECT h.id, h.name, h.dock_id FROM Hauler h"
            query_results = db_get_all(sql)
            haulers = [dict(row) for row in query_results]
            serialized_haulers = json.dumps(haulers)

            return handler.response(serialized_haulers, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Hauler WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, hauler_data, pk):
        sql = """
        UPDATE Hauler
        SET
            name = ?,
            dock_id = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (hauler_data['name'], hauler_data['dock_id'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def insert(self, handler, hauler_data):
        sql = """
        INSERT INTO Hauler (name, dock_id) VALUES (?, ?)
        """
    
        new_item = db_create(sql, (hauler_data['name'], hauler_data['dock_id']))
    
        if new_item is not None:
        # Build a response dictionary with the created resource's ID
            response_data = {
                "id": new_item,
                "name": hauler_data['name'],
                "dock_id": hauler_data['dock_id']
            }
        
            return handler.response(response_data, status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)
        