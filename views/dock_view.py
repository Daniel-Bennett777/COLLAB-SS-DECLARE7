import json
from nss_handler import status
from repository import db_get_single, db_get_all, db_delete, db_update, db_create

class DocksView():

    def get(self, handler, pk):
        if pk != 0:
            sql = """
            SELECT
                d.id,
                d.location,
                d.capacity
            FROM Dock d
            WHERE d.id = ?
            """
            query_results = db_get_single(sql, pk)
            serialized_hauler = json.dumps(dict(query_results))

            return handler.response(serialized_hauler, status.HTTP_200_SUCCESS.value)
        else:

            query_results = db_get_all("SELECT d.id, d.location, d.capacity FROM Dock d")
            haulers = [dict(row) for row in query_results]
            serialized_haulers = json.dumps(haulers)

            return handler.response(serialized_haulers, status.HTTP_200_SUCCESS.value)

    def delete(self, handler, pk):
        number_of_rows_deleted = db_delete("DELETE FROM Dock WHERE id = ?", pk)

        if number_of_rows_deleted > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

    def update(self, handler, dock_data, pk):
        sql = """
        UPDATE Dock
        SET
            location = ?,
            capacity = ?
        WHERE id = ?
        """
        number_of_rows_updated = db_update(
            sql,
            (dock_data['location'], dock_data['capacity'], pk)
        )

        if number_of_rows_updated > 0:
            return handler.response("", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)
        else:
            return handler.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
    def insert(self, handler, dock_data):
        sql = """
        INSERT INTO Dock (location, capacity) VALUES (?, ?)
        """
    
        new_item = db_create(sql, (dock_data['location'], dock_data['capacity']))
    
        if new_item is not None:
        # Build a response dictionary with the created resource's ID
            response_data = {
                "id": new_item,
                "location": dock_data['location'],
                "capacity": dock_data['capacity']
            }
        
            return handler.response(json.dumps(response_data), status.HTTP_201_SUCCESS_CREATED.value)
        else:
            return handler.response("", status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value)
        